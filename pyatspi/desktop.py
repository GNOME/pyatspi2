#Copyright (C) 2008 Codethink Ltd

#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License version 2 as published by the Free Software Foundation.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU Lesser General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from interfaces import *
from accessible import BaseProxy, BoundingBox
from state import StateSet

from role import ROLE_UNKNOWN
from component import LAYER_WIDGET

__all__ = [
           "Desktop",
          ]

#------------------------------------------------------------------------------

class DesktopComponent(object):
        """
        The Component interface is implemented by objects which occupy
        on-screen space, e.g. objects which have onscreen visual representations.
        The methods in Component allow clients to identify where the
        objects lie in the onscreen coordinate system, their relative
        size, stacking order, and position. It also provides a mechanism
        whereby keyboard focus may be transferred to specific user interface
        elements programmatically. This is a 2D API, coordinates of 3D
        objects are projected into the 2-dimensional screen view for
        purposes of this interface.
        """

        def contains(self, *args, **kwargs):
                """
                @return True if the specified point lies within the Component's
                bounding box, False otherwise.
                """
                return False

        def getAccessibleAtPoint(self, *args, **kwargs):
                """
                @return the Accessible child whose bounding box contains the
                specified point.
                """
                return None

        def getAlpha(self, *args, **kwargs):
                """
                Obtain the alpha value of the component. An alpha value of 1.0
                or greater indicates that the object is fully opaque, and an
                alpha value of 0.0 indicates that the object is fully transparent.
                Negative alpha values have no defined meaning at this time.
                """
                return 1.0

        def getExtents(self, coord_type):
                """
                Obtain the Component's bounding box, in pixels, relative to the
                specified coordinate system. 
                @param coord_type
                @return a BoundingBox which entirely contains the object's onscreen
                visual representation.
                """
                #TODO This needs to return the window size
                return BoundingBox(*(0,0,1024,768))

        def getLayer(self, *args, **kwargs):
                """
                @return the ComponentLayer in which this object resides.
                """
                return LAYER_WIDGET

        def getMDIZOrder(self):
                """
                Obtain the relative stacking order (i.e. 'Z' order) of an object.
                Larger values indicate that an object is on "top" of the stack,
                therefore objects with smaller MDIZOrder may be obscured by objects
                with a larger MDIZOrder, but not vice-versa. 
                @return an integer indicating the object's place in the stacking
                order.
                """
                return 0

        def getPosition(self, coord_type):
                """
                Obtain the position of the current component in the coordinate
                system specified by coord_type. 
                @param : coord_type
                @param : x
                an out parameter which will be back-filled with the returned
                x coordinate. 
                @param : y
                an out parameter which will be back-filled with the returned
                y coordinate.
                """
                return (0,0)

        def getSize(self, *args, **kwargs):
                """
                Obtain the size, in the coordinate system specified by coord_type,
                of the rectangular area which fully contains the object's visual
                representation, without accounting for viewport clipping. 
                @param : width
                the object's horizontal extents in the specified coordinate system.
                @param : height
                the object's vertical extents in the specified coordinate system.
                """
                #TODO Need to return window size
                return (1024, 768)

        def grabFocus(self, *args, **kwargs):
                """
                Request that the object obtain keyboard focus.
                @return True if keyboard focus was successfully transferred to
                the Component.
                """
                return False

#------------------------------------------------------------------------------

class Desktop (BaseProxy):
        """
        Desktop object is an accessible whose children are the root accessible
        objects of all applications on the desktop. (Connected to ATSPI)
        """

        def getApplication(self):
                return None

        def getAttributes(self):
                return []

        def getChildAtIndex(self, index):
                func = self.get_dbus_method("getApplications", dbus_interface=ATSPI_REGISTRY_INTERFACE)
                apps = func()
                return self.acc_factory.create_application(apps[index])

        def getIndexInParent(self):
                return -1

        def getLocalizedRoleName(self):
                #TODO Need to localize this somehow.
                return 'unknown'

        def getRelationSet(self):
                return []

        def getRole(self):
                return ROLE_UNKNOWN

        def getRoleName(self):
                return 'unknown'

        def getState(self):
                return StateSet()

        def get_childCount(self):
                func = self.get_dbus_method("getApplications", dbus_interface=ATSPI_REGISTRY_INTERFACE)
                apps = func()
                return len(apps)

        def get_description(self):
                return ''

        def get_name(self):
                return 'main'

        def get_parent(self):
                return None

        def queryInterface(self, interface):
                """
                Gets a different accessible interface for this object
                or raises a NotImplemented error if the given interface
                is not supported.
                """
                if interface == ATSPI_ACCESSIBLE:
                                return self
                elif interface == ATSPI_COMPONENT:
                                return DesktopComponent()
                else:
                                raise NotImplementedError(
                                                "%s not supported by accessible object at path %s"
                                                % (interface, self._acc_path))

#------------------------------------------------------------------------------

class DesktopTest (Desktop):

        def getChildAtIndex(self, index):
                return self.acc_factory.create_application(self.app_name)

        def get_childCount(self):
                return 1

#------------------------------------------------------------------------------

class DesktopCached(Desktop):
        """
        Desktop object is an accessible whose children are the root accessible
        objects of all applications on the desktop. (Connected to ATSPI)
        """

        def __init__(self, cache, *args):
                BaseProxy.__init__(self, *args);

                self.cache = cache

        def getChildAtIndex(self, index):
                app_name = self.cache.application_list[index]
                acc_path = self.cache.application_cache[app_name].root

                return self.acc_factory.create_application(app_name)

        def get_childCount(self):
                return len(self.cache.application_list)

#END----------------------------------------------------------------------------
