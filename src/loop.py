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

from registry import Registry
from factory import CachedObjectFactory
from appevent import _ApplicationEventRegister
from deviceevent import DeviceEventRegister

__all__ = ["new_registry"]

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

def new_registry (type):
        """
        Factory method for creating the registry
        and configuring it for different main loops.
        """ 

        if type == "GObject":
                devreg = DeviceEventRegister()
                appreg = _ApplicationEventRegister()

                connection = dbus.SessionBus()
                factory = CachedObjectFactory(connection, GObjectProxy)

                loop = GObjectMain ()
                
                return Registry (devreg, appreg, factory, loop)
        else
                raise Exception ("Don't know the type of main loop")
