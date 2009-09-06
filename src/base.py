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

__all__ = [
           "BaseProxy",
          ]

#------------------------------------------------------------------------------

class BaseProxyMeta(type):
        def __new__(meta, *args, **kwargs):
                cls = type.__new__(meta, *args, **kwargs)

                queryable_interfaces = { 
                        'Accessible':interfaces.ATSPI_ACCESSIBLE,
                        'Action':interfaces.ATSPI_ACTION,
                        'Application':interfaces.ATSPI_APPLICATION,
                        'Collection':interfaces.ATSPI_COLLECTION,
                        'Component':interfaces.ATSPI_COMPONENT,
                        'Desktop':interfaces.ATSPI_DESKTOP,
                        'Document':interfaces.ATSPI_DOCUMENT,
                        'EditableText':interfaces.ATSPI_EDITABLE_TEXT,
                        'Hypertext':interfaces.ATSPI_HYPERTEXT,
                        'Hyperlink':interfaces.ATSPI_HYPERLINK,
                        'Image':interfaces.ATSPI_IMAGE,
                        'Selection':interfaces.ATSPI_SELECTION,
                        'StreamableContent':interfaces.ATSPI_STREAMABLE_CONTENT,
                        'Table':interfaces.ATSPI_TABLE,
                        'Text':interfaces.ATSPI_TEXT,
                        'Value':interfaces.ATSPI_VALUE,
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

class BaseProxy(object):

        __metaclass__ = BaseProxyMeta

        def __init__(self, app_name, acc_path, acc_factory, dbus_interface, dbus_object):
                """
                Create a D-Bus Proxy for an ATSPI interface.

                app_name - D-Bus bus name of the application this accessible belongs to.
                acc_path - D-Bus object path of the server side accessible object.
                acc_factory - Factory used to create new accessible objects.
                dbus_object - The D-Bus proxy object used by the accessible for D-Bus method calls.
                """
                self._app_name = app_name
                self._acc_path = acc_path
                self._acc_factory = acc_factory
                self._dbus_interface = dbus_interface
                self._dbus_object = dbus_object

                self._pgetter = self.get_dbus_method("Get",
                                                     dbus_interface="org.freedesktop.DBus.Properties")
                self._psetter = self.get_dbus_method("Set",
                                                     dbus_interface="org.freedesktop.DBus.Properties")

        @property
        def app_name (self):
                return self._app_name

        @property
        def acc_path (self):
                return self._acc_path

        @property
        def acc_factory (self):
                return self._acc_factory

        @property
        def dbus_interface (self):
                return self._dbus_interface

        @property
        def dbus_object (self):
                return self._dbus_object

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

        @property
        def interfaces:
                """
                Returns the interfaces supported by this object.
                """
                return []

        def queryInterface(self, interface):
                """
                Gets a different accessible interface for this object
                or raises a NotImplemented error if the given interface
                is not supported.
                """
                if interface in self.interfaces:
                        return self.acc_factory.create_accessible(self.app_name,
                                                                  self.acc_path,
                                                                  interface,
                                                                  dbus_object=self.dbus_object)
                else:
                        raise NotImplementedError(
                                "%s not supported by accessible object at path %s"
                                % (interface, self._acc_path))

#END----------------------------------------------------------------------------
