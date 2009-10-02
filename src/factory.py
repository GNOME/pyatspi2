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

from cache import ApplicationCache

#------------------------------------------------------------------------------

class CachedAccessibleFactory (object):

        def __init__ (self, event_dispatcher, connection, proxy_class):

                self._cache = ApplicationCache(event_dispatcher, connection)

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
                        interfaces.ATSPI_EDITABLE_TEXT:Text,
                        interfaces.ATSPI_HYPERTEXT:Hypertext,
                        interfaces.ATSPI_HYPERLINK:Hyperlink,
                        interfaces.ATSPI_IMAGE:Image,
                        interfaces.ATSPI_SELECTION:Selection,
                        interfaces.ATSPI_TABLE:Table,
                        interfaces.ATSPI_TEXT:Text,
                        interfaces.ATSPI_VALUE:Value,
                }


        def create_accessible (self, name, path, itf, object=None):
                """
                Creates an accessible object.

                @name: D-Bus name of the application where the accessible object resides.

                @path: D-Bus path of the object within the application.

                @itf: D-Bus interface of the requested object. A different accessible object
                            class will be created depending on this. Making the function much like 
                            an accessible object factory.

                @object: If a D-Bus object already exists for the accessible object it can be
                              provided here so that another one is not created.
                """
                if name == ATSPI_REGISTRY_NAME or path == ATSPI_DESKTOP_PATH:
                        itf = interfaces.ATSPI_DESKTOP

                if object == None:
                        object = self._proxy_class (self._connection, name, path, introspect=False)

                if (itf == interfaces.ATSPI_DESKTOP):
                        impl = Desktop (name, path, self, itf, object)
                else:
                        impl = AccessibleImplCached (self._cache, name, path, self, itf, object)

                return self._interfaces [interface] (impl, name, path, self, itf, object)

#END----------------------------------------------------------------------------
