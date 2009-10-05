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
from table import *
from value import *

from desktop import DesktopTest
from accessible import AccessibleImpl

import dbus

#------------------------------------------------------------------------------

class CachedAccessibleFactory (object):

        def __init__ (self, cache, connection, proxy_class):

                self._cache = cache
                self._connection = connection
                self._proxy_class = proxy_class

                self._interfaces = { 
                        interfaces.ATSPI_ACCESSIBLE:Accessible,
                        interfaces.ATSPI_ACTION:Action,
                        interfaces.ATSPI_APPLICATION:Application,
                        interfaces.ATSPI_COLLECTION:Collection,
                        interfaces.ATSPI_COMPONENT:Component,
                        interfaces.ATSPI_DESKTOP:Accessible,
                        interfaces.ATSPI_DOCUMENT:Document,
                        interfaces.ATSPI_EDITABLE_TEXT:EditableText,
                        interfaces.ATSPI_HYPERTEXT:Hypertext,
                        interfaces.ATSPI_HYPERLINK:Hyperlink,
                        interfaces.ATSPI_IMAGE:Image,
                        interfaces.ATSPI_SELECTION:Selection,
                        interfaces.ATSPI_TABLE:Table,
                        interfaces.ATSPI_TEXT:Text,
                        interfaces.ATSPI_VALUE:Value,
                }

        def create_application (self, name):
                root= self._cache.application_list[name].root
                dbus_object = self._proxy_class (self._connection, name, root, introspect=False)

                impl = AccessibleImplCached (self._cache, name, root, self, interfaces.ACCESSIBLE, dbus_object)
                return Application (impl, name, root, self, interfaces.ATSPI_APPLICATION, dbus_object)

        def create_accessible (self, name, path, itf, dbus_object=None):
                if dbus_object == None:
                        dbus_object = self._proxy_class (self._connection, name, path, introspect=False)

                if name == interfaces.ATSPI_REGISTRY_NAME or path == interfaces.ATSPI_DESKTOP_PATH:
                        impl = DesktopCached (self._cache, name, path, self, itf, dbus_object)
                else:
                        impl = AccessibleImplCached (self._cache, name, path, self, itf, dbus_object)

                return self._interfaces[itf] (impl, name, path, self, itf, dbus_object)

#------------------------------------------------------------------------------

class AccessibleFactory (object):

        _PATH = '/org/freedesktop/atspi/tree'
        _INTERFACE = 'org.freedesktop.atspi.Tree'

        def __init__ (self, app_name, connection, proxy_class):

                self._app_name = app_name
                self._connection = connection
                self._proxy_class = proxy_class

                self._interfaces = { 
                        interfaces.ATSPI_ACCESSIBLE:Accessible,
                        interfaces.ATSPI_ACTION:Action,
                        interfaces.ATSPI_APPLICATION:Application,
                        interfaces.ATSPI_COLLECTION:Collection,
                        interfaces.ATSPI_COMPONENT:Component,
                        interfaces.ATSPI_DESKTOP:Accessible,
                        interfaces.ATSPI_DOCUMENT:Document,
                        interfaces.ATSPI_EDITABLE_TEXT:EditableText,
                        interfaces.ATSPI_HYPERTEXT:Hypertext,
                        interfaces.ATSPI_HYPERLINK:Hyperlink,
                        interfaces.ATSPI_IMAGE:Image,
                        interfaces.ATSPI_SELECTION:Selection,
                        interfaces.ATSPI_TABLE:Table,
                        interfaces.ATSPI_TEXT:Text,
                        interfaces.ATSPI_VALUE:Value,
                }

        def create_application (self, name):
                obj = self._connection.get_object(name, self._PATH, introspect=False)
                itf = dbus.Interface(obj, self._INTERFACE)
                root = itf.getRoot()
                dbus_object = self._proxy_class (self._connection, name, root, introspect=False)

                impl = AccessibleImpl (name, root, self, interfaces.ATSPI_ACCESSIBLE, dbus_object)
                return Application (impl, name, root, self, interfaces.ATSPI_APPLICATION, dbus_object)

        def create_accessible (self, name, path, itf, dbus_object=None):
                if dbus_object == None:
                        dbus_object = self._proxy_class (self._connection, name, path, introspect=False)

                if name == interfaces.ATSPI_REGISTRY_NAME or path == interfaces.ATSPI_DESKTOP_PATH:
                        obj = self._connection.get_object(self._app_name, self._PATH, introspect=False)
                        tree = dbus.Interface(obj, self._INTERFACE)
                        root = tree.getRoot()

                        dbus_object = self._proxy_class (self._connection,
                                                         self._app_name,
                                                         root,
                                                         introspect=False)
                        impl = DesktopTest (self._app_name, root, self, interfaces.ATSPI_DESKTOP, dbus_object)
                else:
                        impl = AccessibleImpl (name, path, self, itf, dbus_object)

                return self._interfaces[itf] (impl, name, path, self, itf, dbus_object)

#END----------------------------------------------------------------------------
