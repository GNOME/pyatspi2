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

class GObjectMain (object):
        def set_main (self):
                from dbus.mainloop.glib import DBusGMainLoop
                DBusGMainLoop (set_as_default=True)
                del DBusGMainLoop
        
        def get_dbus_method (self);
                pass
