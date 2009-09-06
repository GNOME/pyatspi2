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

import interfaces

from accessible import *
from action import *
from application import *
from collection import *
from component import *
from desktop import *
from document import *
from editabletext import *
from hyperlink import *
from hypertext import *
from image import *
from selection import *
from state import *
from text import *
from value import *

from cache import ApplicationCache

#------------------------------------------------------------------------------

class CachedAccessibleFactory (object):

        def __init__ (self, connection, proxy_class):

                self._cache = ApplicationCache()

                self._connection = connection
                self._proxy_class = proxy_class

                self._interfaces = { 
                        interfaces.ATSPI_ACTION:Action,
                        interfaces.ATSPI_APPLICATION:Application,
                        interfaces.ATSPI_COLLECTION:Collection,
                        interfaces.ATSPI_COMPONENT:Component,
                        interfaces.ATSPI_DOCUMENT:Document,
                        interfaces.ATSPI_EDITABLE_TEXT:Text,
                        interfaces.ATSPI_HYPERTEXT:Hypertext,
                        interfaces.ATSPI_HYPERLINK:Hyperlink,
                        interfaces.ATSPI_IMAGE:Image,
                        interfaces.ATSPI_SELECTION:Selection,
                        interfaces.ATSPI_TABLE:Table,
                        interfaces.ATSPI_TEXT:Text,
                        interfaces.ATSPI_VALUE:Value,
                }

                for value in self._interfaces.values():
                        value.__bases__.append(Accessible)

                self._interfaces[interfaces.ATSPI_ACCESSIBLE] = Accessible
                self._interfaces[interfaces.ATSPI_DESKTOP] = Desktop

        def create_accessible (self, app_name, acc_path, interface, dbus_object=None):
                """
                Creates an accessible object.

                @app_name: D-Bus name of the application where the accessible object resides.

                @acc_path: D-Bus path of the object within the application.

                @interface: D-Bus interface of the requested object. A different accessible object
                            class will be created depending on this. Making the function much like 
                            an accessible object factory.

                @dbus_object: If a D-Bus object already exists for the accessible object it can be
                              provided here so that another one is not created.
                """
                if dbus_object == None:
                        dbus_object = self._proxy_class (self._connection, bus_name, object_path, introspect=False)

                if app_name == ATSPI_REGISTRY_NAME or acc_path == ATSPI_DESKTOP_PATH:
                        return self._interfaces [ATSPI_DESKTOP] (app_name,
                                                                 acc_path,
                                                                 self,
                                                                 interface,
                                                                 dbus_object,
                                                                 self._cache)

                return self._interfaces [interface] (app_name,
                                                     acc_path,
                                                     self,
                                                     interface,
                                                     dbus_object,
                                                     self._cache)

#END----------------------------------------------------------------------------
