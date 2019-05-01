#!/usr/bin/python

# magFocusTracker
#
# Copyright 2009 Sun Microsystems Inc.
# Copyright 2010 Willie Walker
# Copyright 2011-2012 Igalia, S. L.
# Copyright 2011-2012 Inclusive Design Research Centre, OCAD University
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.
#
# * Contributor: Joanie Diggs <diggs@igalia.com>
# * Contributor: Joseph Scheuhammer <clown@alum.mit.edu>

"""Proof-of-concept standalone application that shows how:
1. to track keyboard focus and the caret using AT-SPI events, and
2. use D-Bus to drive the magnifier to insure the tracked object is
   within the magnified view.
"""

__copyright__ = \
  "Copyright (c) 2009 Sun Microsystems Inc." \
  "Copyright (c) 2010 Willie Walker" \
  "Copyright (c) 2011-2012 Igalia, S.L." \
  "Copyright (c) 2011-2012 Inclusive Design Research Centre, OCAD University"
__license__   = "LGPL"

import dbus
import pyatspi
import sys
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import Gdk
from gi.repository.Gio import Settings

_screenWidth = 0
_screenHeight = 0
_magnifier = None
_zoomer = None

class RoiHandler:
    """For handling D-Bus calls to zoomRegion.getRoi() asynchronously"""

    def __init__(self, left=0, top=0, width=0, height=0, centerX=0, centerY=0,
                 edgeMarginX=0, edgeMarginY=0):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        self.edgeMarginX = edgeMarginX
        self.edgeMarginY = edgeMarginY

    def setRoiCenter(self, reply):
        """Given a region of interest, put that at the center of the magnifier.

        Arguments:
        - reply:  an array defining a rectangle [left, top, right, bottom]
        """
        roiWidth = reply[2] - reply[0]
        roiHeight = reply[3] - reply[1]
        if self.width > roiWidth:
            self.centerX = self.left
        if self.height > roiHeight:
            self.centerY = self.top
        _setROICenter(self.centerX, self.centerY)

    def setRoiCursorPush(self, reply):
        """Given a region of interest, nudge it if the caret or control is not
        visible.

        Arguments:
        - reply:  an array defining a rectangle [left, top, right, bottom]
        """

        roiLeft = reply[0]
        roiTop = reply[1]
        roiWidth = reply[2] - roiLeft
        roiHeight = reply[3] - roiTop
        leftOfROI = (self.left - self.edgeMarginX) <= roiLeft
        rightOfROI = \
            (self.left + self.width + self.edgeMarginX) >= (roiLeft + roiWidth)
        aboveROI = (self.top - self.edgeMarginY)  <= roiTop
        belowROI = \
            (self.top + self.height + self.edgeMarginY) >= (roiTop + roiHeight)

        x1 = roiLeft
        x2 = roiLeft + roiWidth
        y1 = roiTop
        y2 = roiTop + roiHeight

        if leftOfROI:
            x1 = max(0, self.left - self.edgeMarginX)
            x2 = x1 + roiWidth
        elif rightOfROI:
            self.left = min(_screenWidth, self.left + self.edgeMarginX)
            if self.width > roiWidth:
                x1 = self.left
                x2 = x1 + roiWidth
            else:
                x2 = self.left + self.width
                x1 = x2 - roiWidth

        if aboveROI:
            y1 = max(0, self.top - self.edgeMarginY)
            y2 = y1 + roiHeight
        elif belowROI:
            self.top = min(_screenHeight, self.top + self.edgeMarginY)
            if self.height > roiHeight:
                y1 = self.top
                y2 = y1 + roiHeight
            else:
                y2 = self.top + self.height
                y1 = y2 - roiHeight

        _setROICenter((x1 + x2) / 2, (y1 + y2) / 2)

    def setRoiCenterErr(self, error):
        _dbusCallbackError('_setROICenter()', error)

    def setRoiCursorPushErr(self, error):
        _dbusCallbackError('_setROICursorPush()', error)

    def magnifyAccessibleErr(self, error):
        _dbusCallbackError('magnifyAccessible()', error)

def _dbusCallbackError(funcName, error):
    """Log D-Bus errors

    Arguments:
    - funcName: The name of the gsmag function that made the D-Bus call.
    - error: The error that D-Bus returned.
    """
    logLine = funcName + ' failed: ' + str(error)
    debug.println(debug.LEVEL_WARNING, logLine)

def _setROICenter(x, y):
    """Centers the region of interest around the given point.

    Arguments:
    - x: integer in unzoomed system coordinates representing x component
    - y: integer in unzoomed system coordinates representing y component
    """
    _zoomer.shiftContentsTo(x, y, ignore_reply=True)

def _setROICursorPush(x, y, width, height):
    """Nudges the ROI if the caret or control is not visible.

    Arguments:
    - x: integer in unzoomed system coordinates representing x component
    - y: integer in unzoomed system coordinates representing y component
    - width: integer in unzoomed system coordinates representing the width
    - height: integer in unzoomed system coordinates representing the height
    """

    roiPushHandler = RoiHandler(x, y, width, height)
    _zoomer.getRoi(reply_handler=roiPushHandler.setRoiCursorPush,
                   error_handler=roiPushHandler.setRoiCursorPushErr)

def magnifyAccessible(event, obj=None, extents=None):
    """Sets the region of interest to the upper left of the given
    accessible, if it implements the Component interface.  Otherwise,
    does nothing.

    Arguments:
    - event: the Event that caused this to be called
    - obj: the accessible
    """

    if event.type.startswith("object:state-changed") and not event.detail1:
        # This object just became unselected or unfocused, and we're not
        # big on nostalgia.
        return

    obj = obj or event.source

    haveSomethingToMagnify = False

    if extents:
        [x, y, width, height] = extents
        haveSomethingToMagnify = True
    elif event and event.type.startswith("object:text-caret-moved"):
        try:
            text = obj.queryText()
            if text and (text.caretOffset >= 0):
                offset = text.caretOffset
                if offset == text.characterCount:
                    offset -= 1
                [x, y, width, height] = \
                    text.getCharacterExtents(offset, 0)
                haveSomethingToMagnify = (width + height > 0)
        except:
            haveSomethingToMagnify = False

        if haveSomethingToMagnify:
            _setROICursorPush(x, y, width, height)
            return

    if not haveSomethingToMagnify:
        try:
            extents = obj.queryComponent().getExtents(0)
            [x, y, width, height] = \
                [extents.x, extents.y, extents.width, extents.height]
            haveSomethingToMagnify = True
        except:
            haveSomethingToMagnify = False

    if haveSomethingToMagnify:
        _setROICursorPush(x, y, width, height)

def startTracking():
    global _screenWidth
    global _screenHeight
    global _magnifier
    global _zoomer

    if _magnifier and _zoomer:
        screen = Gdk.Screen.get_default()
        _screenWidth = screen.width()
        _screenHeight = screen.height()

        pyatspi.Registry.registerEventListener(magnifyAccessible,
                                               "object:text-caret-moved",
                                               "object:state-changed:focused",
                                               "object:state-changed:selected")

def stopTracking():
    pyatspi.Registry.deregisterEventListener(magnifyAccessible,
                                             "object:text-caret-moved",
                                             "object:state-changed:focused",
                                             "object:state-changed:selected")

def onEnabledChanged(gsetting, key):
    if key != 'screen-magnifier-enabled':
        return

    enabled = gsetting.get_boolean(key)
    if enabled:
        startTracking()
    else:
        stopTracking()

def _initMagDbus():
    global _magnifier
    global _zoomer

    available = False
    try:
        bus = dbus.SessionBus(mainloop=DBusGMainLoop())
        proxy = \
          bus.get_object('org.gnome.Magnifier', '/org/gnome/Magnifier')
        _magnifier = dbus.Interface(proxy, 'org.gnome.Magnifier')
        zoomerPaths = _magnifier.getZoomRegions()
        if zoomerPaths:
            proxy = bus.get_object('org.gnome.Magnifier', zoomerPaths[0])
            _zoomer = dbus.Interface(proxy, 'org.gnome.Magnifier.ZoomRegion')
            available = True
    except:
        available = False

    return available

def main():
    magServiceAvailable = _initMagDbus()
    if magServiceAvailable:
        a11yAppSettings = Settings('org.gnome.desktop.a11y.applications')
        a11yAppSettings.connect('changed', onEnabledChanged)
        if a11yAppSettings.get_boolean('screen-magnifier-enabled'):
            startTracking()
        pyatspi.Registry.start()
    else:
        print('Magnification service not available. Exiting.')

    return 0

if __name__ == "__main__":
    sys.exit(main())
