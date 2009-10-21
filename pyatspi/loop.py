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

import gobject
import dbus
import os as _os


__all__ = ["GObjectMain",
           "GObjectProxy",
           "NullMain"]

class NullMain (object):
        def __init__ (self):
                pass
        
        def run (self):
                pass

        def stop (self):
                pass

class GObjectMain (object):
        def __init__ (self):
                from dbus.mainloop.glib import DBusGMainLoop
                DBusGMainLoop (set_as_default=True)
                del DBusGMainLoop
        
        def run (self):
                gobject.MainLoop.run()

        def stop (self):
                gobject.MainLoop.quit()

class GObjectProxy (dbus.connection.ProxyObject):
        
        def get_dbus_method (self, *args, **kwargs):
                method = dbus.connection.ProxyObject.get_dbus_method (self, *args, **kwargs)

                loop        = gobject.MainLoop ()
                error       = None
                return_args = []

                def method_error_callback (e):
                        error = e
                        loop.quit ()

                def method_reply_callback (*iargs):
                        return_args = iargs
                        loop.quit ()
                
                def dbus_method_func (*iargs, **ikwargs):
                        #kwargs["reply_handler"] = method_reply_callback
                        #kwargs["error_handler"] = method_error_callback
                        return method (*iargs, **ikwargs)

                        #loop.run()

                        #if error:
                        #        raise error

                        #return return_args

                return dbus_method_func
