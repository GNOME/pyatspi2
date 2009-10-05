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
from cache import *

__all__ = ["build_registry"]

class GObjectMain (object):
        def __init__ (self):
                from dbus.mainloop.glib import DBusGMainLoop
                DBusGMainLoop (set_as_default=True)
                del DBusGMainLoop
        
        def run (self):
                import gobject
                gobject.MainLoop.run()
                del gobject

        def stop (self):
                import gobject
                gobject.MainLoop.quit()
                del gobject

class GObjectProxy (dbus.connection.ProxyObject):
        pass

def build_registry (type):
        """
        Method for creating the registry and configuring it for different main loops.
        """ 

        app_name = None
        if "ATSPI_TEST_APP_NAME" in _os.environ.keys():
                app_name = _os.environ["ATSPI_TEST_APP_NAME"]
                type = "Test"

        if type == "GObject":
                loop = GObjectMain ()

                devreg = _DeviceEventRegister()
                appreg = _ApplicationEventRegister()

                connection = dbus.SessionBus()

                cache = ApplicationCache(appreg, connection)
                factory = CachedAccessibleFactory(cache, connection, GObjectProxy)
                
                return Registry (devreg, appreg, factory, loop)
        elif type == "Test":
                loop = GObjectMain ()
                
                devreg = _NullDeviceEventRegister()
                appreg = _NullApplicationEventRegister()

                connection = dbus.SessionBus()

                factory = AccessibleFactory(app_name, connection, GObjectProxy)

                return Registry (devreg, appreg, factory, loop)
        else:
                raise Exception ("Don't know the type of main loop")
