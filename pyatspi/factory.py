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

import dbus

from busutils import AccessibilityBus

__all__ = [
           "AccessibleFactory"
          ]

#------------------------------------------------------------------------------

class _AccessibleFactory (object):

        def __init__ (self):

                self._connection = AccessibilityBus() 

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

                self._cache = None
                self._desktop = None

	def set_cache (self, cache):
		self._cache = cache

	def set_desktop (self, desktop):
		self._desktop = desktop

        def __call__ (self, name, path, itf, dbus_object=None):
                if dbus_object == None:
                        dbus_object = self._connection.get_object (name, path)
        
                # Hack to link applications 'parent' property up to the desktop object.
                if name == interfaces.ATSPI_REGISTRY_NAME or path == interfaces.ATSPI_DESKTOP_PATH:
                        return self._desktop
                else:
                        return self._interfaces[itf] (self._cache, self, name, path, dbus_object)

class AccessibleFactory (_AccessibleFactory):
	"""
	Shared instance of the D-Bus bus used for accessibility.
	"""

	_shared_instance = None
	
	def __new__ (cls):
		if AccessibleFactory._shared_instance:
			return AccessibleFactory._shared_instance
		else:
			AccessibleFactory._shared_instance = _AccessibleFactory.__new__ (cls)
			return AccessibleFactory._shared_instance

	def __init__ (self):
		_AccessibleFactory.__init__ (self)

#END----------------------------------------------------------------------------
