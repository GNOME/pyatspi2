#Copyright (C) 2009 Codethink Ltd

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

import dbus
import os as _os

from registry import Registry
from factory import CachedAccessibleFactory, AccessibleFactory
from appevent import _ApplicationEventRegister, _NullApplicationEventRegister
from deviceevent import _DeviceEventRegister, _NullDeviceEventRegister
from desktop import *
from cache import *
from loop import *

__all__ = ["set_default_registry",
           "MAIN_LOOP_GLIB",
           "MAIN_LOOP_NONE",
           "MAIN_LOOP_QT"]

MAIN_LOOP_GLIB = 'GLib'
MAIN_LOOP_NONE = 'None'
MAIN_LOOP_QT   = 'Qt'

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop (set_as_default=True)

def get_registry (main_loop_type, app_name=None):
        """
        Creates a new 'Registry' object and sets this object
        as the default returned by pyatspi.Registry.

        The default registry (without calling this function) uses the
        GLib main loop with caching. It connects to a registry daemon.

        This function should be called before pyatspi is used if you
        wish to change these defaults.

        @param main_loop_type: 'GLib', 'None' or 'Qt'. If 'None' is selected then caching
                               is disabled.

        @param use_registry: Whether to connect to a registry daemon for device events.
                             Without this the application to connect to must be declared in the
                             app_name parameter.

        @param app_name: D-Bus name of the application to connect to when not using the registry daemon.
        """
        connection = dbus.SessionBus()

        # Set up the main loop
        if main_loop_type == MAIN_LOOP_GLIB:
                loop   = GObjectMain()
                proxy  = GObjectProxy
        elif main_loop_type == MAIN_LOOP_NONE:
                loop    = NullMain()
                proxy  = dbus.connection.ProxyObject
        else:
                raise Exception ("Unknown main loop specified")

        # Set up the device event controllers
        if app_name:
                devreg = _NullDeviceEventRegister()
                appreg = _NullApplicationEventRegister()
        else:
                devreg = _DeviceEventRegister(connection)
                appreg = _ApplicationEventRegister(connection)

        # Set up the cache / desktop and accesible factories.
        if main_loop_type == MAIN_LOOP_GLIB:
                if app_name:
                        cache = AccessibleCache(appreg, connection, app_name)
                else:
                        cache = ApplicationCache(appreg, connection)
                appreg.setCache (cache)
                factory = CachedAccessibleFactory (cache, connection, proxy)
                desktop = CachedDesktop (cache, factory)

        elif main_loop_type == MAIN_LOOP_NONE:
                factory = AccessibleFactory(connection, proxy)
                if app_name:
                        desktop = TestDesktop (connection, app_name, factory)
                else:
                        desktop = Desktop (connection, factory)

        else:
                raise Exception ("Unknown main loop specified")

        # Create the registry object
        return Registry (devreg, appreg, desktop, factory, loop)

def set_default_registry (main_loop, app_name=None):
        import Accessibility
        Accessibility.Registry = get_registry (main_loop, app_name)
        del Accessibility
