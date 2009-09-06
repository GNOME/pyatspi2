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
from relation import *
from role import *
from selection import *
from state import *
from table import *
from text import *
from value import *

#------------------------------------------------------------------------------

class AccessibleObjectNoLongerExists(Exception):
        pass

#------------------------------------------------------------------------------

class _DBusObjectFactory:

        def __init__(self, connection):

        def get_dbus_object(self, *args, **kwargs):
                pass

        def get_dbus_method(self, *args, **kwargs):
                method =  self.dbus_object.get_dbus_method(*args, **kwargs)

                def dbus_method_func(*iargs, **ikwargs):
                        # TODO Need to throw an AccessibleObjectNoLongerExists exception
                        # on D-Bus error of the same type.
                        try:
                                return method(*iargs, **ikwargs)
                        except UnknownMethodException, e:
                                raise NotImplementedError(e)
                        except DBusException, e:
                                raise LookupError(e)
        
                return dbus_method_func

#------------------------------------------------------------------------------

class _CachedAccessibleFactory (object):

        def __init__ (self, object_factory):

                self._cache = ApplicationCache()

                self._object_factory = object_factory

                self._interfaces = { 
                        interfaces.ATSPI_ACTION:
                        interfaces.ATSPI_APPLICATION:
                        interfaces.ATSPI_COLLECTION:
                        interfaces.ATSPI_COMPONENT:
                        interfaces.ATSPI_DOCUMENT:
                        interfaces.ATSPI_EDITABLE_TEXT:
                        interfaces.ATSPI_HYPERTEXT:
                        interfaces.ATSPI_HYPERLINK:
                        interfaces.ATSPI_IMAGE:
                        interfaces.ATSPI_SELECTION:
                        interfaces.ATSPI_STREAMABLE_CONTENT:
                        interfaces.ATSPI_TABLE:
                        interfaces.ATSPI_TEXT:
                        interfaces.ATSPI_VALUE:
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
                        dbus_object = self._object_factory.get_dbus_object (app_name, acc_path)

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
