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

from interfaces import *
from enum import Enum

from state import *
from state import _marshal_state_set
from relation import _marshal_relation_set
from role import Role, ROLE_NAMES

from dbus.types import UInt32, Int32
from dbus import UnknownMethodException, DBusException

from exceptions import *

import registry
import dbus

__all__ = [
           "LOCALE_TYPE",
           "LOCALE_TYPE_COLLATE",
           "LOCALE_TYPE_CTYPE",
           "LOCALE_TYPE_MESSAGES",
           "LOCALE_TYPE_MONETARY",
           "LOCALE_TYPE_NUMERIC",
           "LOCALE_TYPE_TIME",
           "BoundingBox",
           "BaseProxy",
           "AccessibleMeta",
           "Accessible",
          ]

#------------------------------------------------------------------------------

class LOCALE_TYPE(Enum):
        _enum_lookup = {
                0:'LOCALE_TYPE_MESSAGES',
                1:'LOCALE_TYPE_COLLATE',
                2:'LOCALE_TYPE_CTYPE',
                3:'LOCALE_TYPE_MONETARY',
                4:'LOCALE_TYPE_NUMERIC',
                5:'LOCALE_TYPE_TIME',
        }

LOCALE_TYPE_COLLATE = LOCALE_TYPE(1)
LOCALE_TYPE_CTYPE = LOCALE_TYPE(2)
LOCALE_TYPE_MESSAGES = LOCALE_TYPE(0)
LOCALE_TYPE_MONETARY = LOCALE_TYPE(3)
LOCALE_TYPE_NUMERIC = LOCALE_TYPE(4)
LOCALE_TYPE_TIME = LOCALE_TYPE(5)

#------------------------------------------------------------------------------

class BoundingBox(list):
        def __new__(cls, x, y, width, height):
                return list.__new__(cls, (x, y, width, height))
        def __init__(self, x, y, width, height):
                list.__init__(self, (x, y, width, height))

        def __str__(self):
                return ("(%d, %d, %d, %d)" % (self.x, self.y, self.width, self.height))

        def _get_x(self):
                return self[0]
        def _set_x(self, val):
                self[0] = val
        x = property(fget=_get_x, fset=_set_x)
        def _get_y(self):
                return self[1]
        def _set_y(self, val):
                self[1] = val
        y = property(fget=_get_y, fset=_set_y)
        def _get_width(self):
                return self[2]
        def _set_width(self, val):
                self[2] = val
        width = property(fget=_get_width, fset=_set_width)
        def _get_height(self):
                return self[3]
        def _set_height(self, val):
                self[3] = val
        height = property(fget=_get_height, fset=_set_height)

#------------------------------------------------------------------------------

class _PropertyCache(dict):
  def wipe(self):
      self.__dict__ = {}

#------------------------------------------------------------------------------

class AccessibleMeta(type):
        def __new__(meta, *args, **kwargs):
                cls = type.__new__(meta, *args, **kwargs)

                queryable_interfaces = { 
                        'Accessible':ATSPI_ACCESSIBLE,
                        'Action':ATSPI_ACTION,
                        'Application':ATSPI_APPLICATION,
                        'Collection':ATSPI_COLLECTION,
                        'Component':ATSPI_COMPONENT,
                        'Desktop':ATSPI_DESKTOP,
                        'Document':ATSPI_DOCUMENT,
                        'EditableText':ATSPI_EDITABLE_TEXT,
                        'Hypertext':ATSPI_HYPERTEXT,
                        'Hyperlink':ATSPI_HYPERLINK,
                        'Image':ATSPI_IMAGE,
                        'Selection':ATSPI_SELECTION,
                        'StreamableContent':ATSPI_STREAMABLE_CONTENT,
                        'Table':ATSPI_TABLE,
                        'Text':ATSPI_TEXT,
                        'Value':ATSPI_VALUE,
                }

                def return_query(interface):
                        def new_query(self):
                                return self.queryInterface(interface)
                        return new_query

                for interface in queryable_interfaces.keys():
                        name = 'query%s' % interface
                        setattr(cls, name, return_query(queryable_interfaces[interface])) 

                return cls

#------------------------------------------------------------------------------

class BaseProxy (object):

        __metaclass__ = AccessibleMeta

        def __init__(self, factory, name, path, dbus_object):
                """
                Create a D-Bus Proxy for an ATSPI interface.

                factory - Factory used to create new accessible objects.
                name - D-Bus bus name of the application this accessible belongs to.
                path - D-Bus object path of the server side accessible object.
                dbus_object - The D-Bus proxy object used by the accessible for D-Bus method calls.
                """
                self._acc_factory = factory
                self._app_name = name
                self._acc_path = path
                self._dbus_object = dbus_object

                self._pgetter = self._dbus_object.get_dbus_method("Get",
                                                     dbus_interface="org.freedesktop.DBus.Properties")
                self._psetter = self._dbus_object.get_dbus_method("Set",
                                                     dbus_interface="org.freedesktop.DBus.Properties")

        @property
        def app_name (self):
                return self._app_name

        @property
        def acc_path (self):
                return self._acc_path

        # Proxy Equality ----------------------------------------------------------

        def __eq__(self, other):
                if other is None:
                        return False
                try:
                        if self.app_name == other.app_name and \
                           self.acc_path == other.acc_path:
                                return True
                        else:
                                return False
                except AttributeError:
                        return False

        # D-Bus method wrapper ----------------------------------------------------------

        def get_dbus_method (self, *args, **kwargs):
                method =  self._dbus_object.get_dbus_method(*args, **kwargs)

                def dbus_method_func(*iargs, **ikwargs):
                        # Need to throw an AccessibleObjectNoLongerExists exception
                        # on D-Bus error of the same type.

                        try:
                                return method(*iargs, **ikwargs)
                        except UnknownMethodException, e:
                                raise NotImplementedError(e)
                        except DBusException, e:
                                raise LookupError(e)
        
                return dbus_method_func

#------------------------------------------------------------------------------

class Accessible(BaseProxy):
        """
        The interface which is implemented by all accessible objects.
        """

        def __init__(self, cache, *args):
                BaseProxy.__init__(self, *args);

		self._cache = cache

                self._relation_set = None
                try:
                        self._soft_cache_data = self._cache.soft[(self._app_name, self._acc_path)]
                except KeyError:
                        self._soft_cache_data = _PropertyCache()
                        self._cache.soft[(self._app_name, self._acc_path)] = self._soft_cache_data

        # Python object protocol --------------------------------------------------------

        def __str__(self):
                    try:
                              return '[%s | %s]' % (self.getRoleName(), self.name)
                    except Exception:
                              return '[DEAD]'

        def __eq__(self, other):
                if other is None:
                        return False
                try:
                        if self.app_name == other.app_name and \
                           self.acc_path == other.acc_path:
                                return True
                        else:
                                return False
                except AttributeError:
                        return False

        def __ne__(self, other):
                return not self.__eq__(other)

        def __hash__(self):
                return hash(self.app_name + self.acc_path)

        def __nonzero__(self):
                return True

        def __len__(self):
                return self.getChildCount()

        def __getitem__(self, index):
                """
                Thin wrapper around getChildAtIndex.
                
                @param index: Index of desired child
                @type index: integer
                @return: Accessible child
                @rtype: Accessibility.Accessible
                """
                n = self.childCount
                if index >= n:
                        raise IndexError
                elif index < -n:
                        raise IndexError
                elif index < 0:
                        index += n
                return self.getChildAtIndex(index)
            
        # Bonobo interface --------------------------------------------------------------

        def queryInterface(self, interface):
                """
                Gets a different accessible interface for this object
                or raises a NotImplemented error if the given interface
                is not supported.
                """
                if interface in self.interfaces or interface == "org.a11y.atspi.Collection":
                        return self._acc_factory (self.app_name, self.acc_path, interface,
                                                                  dbus_object=self._dbus_object)
                else:
                        raise NotImplementedError(
                                "%s not supported by accessible object at path %s"
                                % (interface, self._acc_path))

        # Cache data --------------------------------------------------------------------

        @property
	def cached (self):
                if not(registry.Registry().started):
                        return False
                if self._cache is not None:
		        return (self.app_name, self.acc_path) in self._cache
                else:
                        return False

        @property
	def _cached_data (self):
                if self._cache is not None:
		        return self._cache[(self.app_name, self.acc_path)]
                else:
                        raise KeyError ()

        # Accessible interface ----------------------------------------------------------

        def getApplication(self):
                """
                Get the containing Application for this object.
                @return the Application instance to which this object belongs.
                """
                if self.cached:
			name, path = self._cached_data.application
		else:
                        func = self.get_dbus_method("GetApplication", dbus_interface=ATSPI_ACCESSIBLE)
			name, path = func ()
		return self._acc_factory (name, path, ATSPI_APPLICATION)

        def getAttributes(self):
                """
                Get a list of properties applied to this object as a whole, as
                an AttributeSet consisting of name-value pairs. As such these
                attributes may be considered weakly-typed properties or annotations,
                as distinct from the strongly-typed interface instance data declared
                using the IDL "attribute" keyword.
                Not all objects have explicit "name-value pair" AttributeSet
                properties.
                Attribute names and values may have any UTF-8 string value, however
                where possible, in order to facilitate consistent use and exposure
                of "attribute" properties by applications and AT clients, attribute
                names and values should chosen from a publicly-specified namespace
                where appropriate.
                Where possible, the names and values in the name-value pairs
                should be chosen from well-established attribute namespaces using
                standard semantics. For example, attributes of Accessible objects
                corresponding to XHTML content elements should correspond to
                attribute names and values specified in the w3c XHTML specification,
                at http://www.w3.org/TR/xhtml2, where such values are not already
                exposed via a more strongly-typed aspect of the AT-SPI API. Metadata
                names and values should be chosen from the 'Dublin Core' Metadata
                namespace using Dublin Core semantics: http://dublincore.org/dcregistry/
                Similarly, relevant structural metadata should be exposed using
                attribute names and values chosen from the CSS2 and WICD specification:
                http://www.w3.org/TR/1998/REC-CSS2-19980512 WICD (http://www.w3.org/TR/2005/WD-WICD-20051121/).

                @return : An AttributeSet encapsulating any "attribute values"
                currently defined for the object. An attribute set is a list of strings
                with each string comprising an name-value pair format 'name:value'.
                """
                func = self.get_dbus_method("GetAttributes", dbus_interface=ATSPI_ACCESSIBLE)
                attr = func ()
                return [key + ':' + value for key, value in attr.items()]

        def getChildAtIndex(self, index):
                """
                Get the accessible child of this object at index. 
                @param : index
                an in parameter indicating which child is requested (zero-indexed).
                @return : the 'nth' Accessible child of this object.
                """
                if self.cached and not(self._cached_data.state[0] & (1 << STATE_MANAGES_DESCENDANTS)):
                        (name, path) = self._cached_data.children[index]
                else:
                        func = self.get_dbus_method("GetChildAtIndex", dbus_interface=ATSPI_ACCESSIBLE)
                        (name, path) = func (index)

                if (path == ATSPI_ROOT_PATH):
                        itf = ATSPI_APPLICATION
                else:
                        itf = ATSPI_ACCESSIBLE
                return self._acc_factory (name, path, itf)

        def getIndexInParent(self):
                """
                Get the index of this object in its parent's child list.
                @return : a long integer indicating this object's index in the
                parent's list.
                """
                parent = self.parent
                if parent == None:
                        return -1
                for i in range(0, parent.childCount):
                        child = parent.getChildAtIndex(i)
                        if self == child:
                                return i
                raise AccessibleObjectNoLongerExists("Child not found within parent")

                #func = self.get_dbus_method("GetIndexInParent", dbus_interface=ATSPI_ACCESSIBLE)
                #return func()

        def getLocalizedRoleName(self):
                """
                Get a string indicating the type of UI role played by this object,
                translated to the current locale.
                @return : a UTF-8 string indicating the type of UI role played
                by this object.
                """
                func = self.get_dbus_method("GetLocalizedRoleName", dbus_interface=ATSPI_ACCESSIBLE)
                return func()

        def getRelationSet(self):
                """
                Get a set defining this object's relationship to other accessible
                objects. 
                @return : a RelationSet defining this object's relationships.
                """
                if self._relation_set is not None:
                        return self._relation_set
                else:
                        func = self.get_dbus_method("GetRelationSet", dbus_interface=ATSPI_ACCESSIBLE)
                        relation_set = func()
                        self._relation_set = _marshal_relation_set(self._acc_factory, self._app_name, relation_set)
                        return self._relation_set

        def getRole(self):
                """
                Get the Role indicating the type of UI role played by this object.
                @return : a Role indicating the type of UI role played by this
                object.
                """
                if self.cached:
                        return Role(self._cached_data.role)
                else:
                        func = self.get_dbus_method("GetRole", dbus_interface=ATSPI_ACCESSIBLE)
                        return Role(self.getSoftCacheItem ("role", func))

        def getRoleName(self):
                """
                Get a string indicating the type of UI role played by this object.
                @return : a UTF-8 string indicating the type of UI role played
                by this object.
                """
                return ROLE_NAMES[self.getRole()]

        def getState(self):
                """
                Get the current state of the object as a StateSet. 
                @return : a StateSet encapsulating the currently true states
                of the object.
                """
                if self.getRole() == 78:
                        print "embedded"
                        return self[0].getState()
                if self.cached:
                        return _marshal_state_set(self._cached_data.state)
                else:
                        func = self.get_dbus_method("GetState", dbus_interface=ATSPI_ACCESSIBLE)
                        try:
                                return _marshal_state_set(self.getSoftCacheItem("state", func))
                        except LookupError:
                                return _marshal_state_set ([1 << STATE_DEFUNCT, 0])

        def isEqual(self, other):
                """
                Determine whether an Accessible refers to the same object as
                another. This method should be used rather than brute-force comparison
                of object references (i.e. "by-value" comparison), as two object
                references may have different apparent values yet refer to the
                same object.
                @param : obj
                an Accessible object reference to compare to 
                @return : a boolean indicating whether the two object references
                point to the same object.
                """
                return self.__eq__(other)

        def _get_childCount(self):
                if self.cached and not(self._cached_data.state[0] & (1 << STATE_MANAGES_DESCENDANTS)):
                        return len(self._cached_data.children)
                else:
                        return Int32(self._pgetter(ATSPI_ACCESSIBLE, "ChildCount"))
        _childCountDoc = \
                """
                childCount: the number of children contained by this object.
                """
        childCount = property(fget=_get_childCount, doc=_childCountDoc)

        getChildCount = _get_childCount

        def _get_description(self):
                if self.cached:
                        return self._cached_data.description
                else:
                        return self._pgetter(ATSPI_ACCESSIBLE, "Description")
        _descriptionDoc = \
                """
                a string describing the object in more detail than name.
                """
        description = property(fget=_get_description, doc=_descriptionDoc)

        def _get_name(self):
                if self.cached:
                        return self._cached_data.name
                else:
                        return self._pgetter(ATSPI_ACCESSIBLE, "Name")
        _nameDoc = \
                """
                a (short) string representing the object's name.
                """
        name = property(fget=_get_name, doc=_nameDoc)

        def _get_parent(self):
                if self.cached:
                        name, path = self._cached_data.parent
                else:
		        name, path = self.getSoftCacheProperty (ATSPI_ACCESSIBLE, "Parent")

                if (path == ATSPI_ROOT_PATH):
                        itf = ATSPI_APPLICATION
                else:
                        itf = ATSPI_ACCESSIBLE
                return self._acc_factory (name, path, itf)
        _parentDoc = \
                """
                an Accessible object which is this object's containing object.
                """
        parent = property(fget=_get_parent, doc=_parentDoc)

        def _get_interfaces(self):
                if self.cached:
                        return self._cached_data.interfaces
                else:
                        func = self.get_dbus_method("GetInterfaces", dbus_interface=ATSPI_ACCESSIBLE)
                        return self.getSoftCacheItem("interfaces", func)
        _interfacesDoc = \
                """
                D-Bus interfaces supported by this accessible object.
                """
        interfaces = property(fget=_get_interfaces, doc=_interfacesDoc)

        # TODO: Possibly merge this with getSoftCacheItem
        def _getConstantProperty(self, interface, name):
                if self.cached:
                        try:
                                getattr(self, "extraData")
                        except (AttributeError):
                                self.extraData = dict()
                        try:
                                return self.extraData[name]
                        except (KeyError):
                                self.extraData[name] = dbus.String(self._pgetter(interface, name))
                                return self.extraData[name]
                return dbus.String(self._pgetter(interface, name))

        def getSoftCacheItem(self, name, func):
                if not(name in self._soft_cache_data):
                        self._soft_cache_data[name] = func()
                return self._soft_cache_data[name]

        def getSoftCacheProperty(self, interface, name):
                if not((interface, name) in self._soft_cache_data):
                        self._soft_cache_data[(interface, name)] = self._pgetter(interface, name)
                return self._soft_cache_data[(interface, name)]

#END----------------------------------------------------------------------------
