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

import os
import dbus

from appevent import Event

from interfaces import *

from busutils import AccessibilityBus

__all__ = [
           "ApplicationCache",
           "AccessibleCache"
          ]

#------------------------------------------------------------------------------

class ApplicationCache(object):
        """
        Keeps a store of the caches for all accessible applications.
        Updates as new applications are added or removed.

        @connection: D-Bus connection used to access applications.
        """

        _APPLICATIONS_ADD = 1
        _APPLICATIONS_REMOVE = 0

        def __init__(self, event_dispatcher=None):
                self._connection = AccessibilityBus ()
                self._factory = None

		self._event_dispatcher = event_dispatcher

                self._application_list = []
                self._application_cache = {}

                self._bus_object = self._connection.get_object("org.freedesktop.DBus",
                                                               "/org/freedesktop/DBus")


                self._regsig = self._connection.add_signal_receiver(self._update_handler,
                                                                    dbus_interface=ATSPI_REGISTRY_INTERFACE,
                                                                    signal_name="UpdateApplications")

                obj = self._connection.get_object(ATSPI_REGISTRY_NAME,
                                                  ATSPI_REGISTRY_PATH)
                self._app_register = dbus.Interface(obj, ATSPI_REGISTRY_INTERFACE)

                apps = self._app_register.GetApplications()

                #this_pid = os.getpid()
                #for app in apps:
                #        that_pid = self._bus_object.GetConnectionUnixProcessID(app)
                #        if not this_pid == that_pid:
                #                self._application_list.append(app)

		self._application_list.extend(apps)
                        
                for bus_name in self._application_list:
                                self._application_cache[bus_name] = AccessibleCache(bus_name)

        def __call__ (self, app_name, acc_path): 
                """
                Returns the cache tuple for the given application and accessible
                object path. Throws an IndexError if the cache data is not found.
                """
                return self._application_cache[app_name][acc_path]

	def __getitem__ (self, key):
		try:
			name, path = key
			return self._application_cache[name][key]
		except Exception:
			raise KeyError ()

        def __contains__ (self, key):
                try:
                        name, path = key
                        return key in self._application_cache[app_name]
                except Exception:
                        return False

        def _update_handler (self, update_type, bus_name):
                if update_type == ApplicationCache._APPLICATIONS_ADD:
                        self._application_list.append(bus_name)
                        self._application_cache[bus_name] = AccessibleCache(bus_name)
			if self._event_dispatcher:
                        	self._event_dispatcher.notifyChildrenChange(ATSPI_REGISTRY_NAME,
                                	                                    ATSPI_DESKTOP_PATH,
									    self._application_cache[bus_name].root, 
                                        	                            True)
                elif update_type == ApplicationCache._APPLICATIONS_REMOVE:
			if self._event_dispatcher:
                        	self._event_dispatcher.notifyChildrenChange(ATSPI_REGISTRY_NAME,
                                	                                    ATSPI_DESKTOP_PATH,
									    self._application_cache[bus_name].root, 
                                        	                            False)
                        self._application_list.remove(bus_name)
                        del(self._application_cache[bus_name])


#------------------------------------------------------------------------------

class _CacheData(object):
        __slots__ = [
                        'path',
                        'application',
                        'parent',
                        'interfaces',
                        'children',
                        'role',
                        'name',
                        'description',
                        'state',
                    ]

        def __init__(self, data):
                self._update(data)

        def __str__(self):
                return (str(self.path) + '\n' +
                        str(self.application) + '\n' +
                        str(self.parent) + '\n' +
                        str(self.children) + '\n' +
                        str(self.interfaces) + '\n' +
                        str(self.name) + '\n' +
                        str(self.role) + '\n' +
                        str(self.description) + '\n' +
                        str(self.state))

        def _update(self, data):
                (self.path,
                 self.application,
                 self.parent,
                 self.children,
                 self.interfaces,
                 self.name,
                 self.role,
                 self.description,
                 self.state) = data

#------------------------------------------------------------------------------

def _list_items_added_removed (l1, l2):
        """
        Returns a tuple (boolean, boolean).
        The first value indicates if, when
        moving from l1 to l2, any items have been added.
        The second value indicates whether any items have
        been removed.
        """
        l1notl2 = [item for item in l1 if item not in l2]
        l2notl1 = [item for item in l2 if item not in l1]
        return ((len(l1notl2) > 0), (len(l2notl1) > 0))

#------------------------------------------------------------------------------

class AccessibleCache(object):
        """
        There is one accessible cache per application.
        For each application the accessible cache stores
        data on every accessible object within the app.

        It also acts as the factory for creating client
        side proxies for these accessible objects.

        connection - DBus connection.
        busName    - Name of DBus connection where cache interface resides.
        """

        _PATH = '/org/at_spi/cache'
        _INTERFACE = 'org.freedesktop.atspi.Cache'
        _GET_METHOD = 'GetItems'
        _UPDATE_SIGNAL = 'UpdateAccessible'
        _REMOVE_SIGNAL = 'RemoveAccessible'

        _ATSPI_EVENT_OBJECT_INTERFACE = "org.freedesktop.atspi.Event.Object"

        _CACHE_PATH = '/org/at_spi/cache'
        _CACHE_INTERFACE = 'org.freedesktop.atspi.Cache'

        def __init__(self, bus_name):
                """
                Creates a cache.

                connection - DBus connection.
                busName    - Name of DBus connection where cache interface resides.
                """
                self._connection = AccessibilityBus()
                self._bus_name = bus_name

                obj = self._connection.get_object(bus_name, self._PATH)
                self._tree_itf = dbus.Interface(obj, self._INTERFACE)

                self._objects = {}

                get_method = self._tree_itf.get_dbus_method(self._GET_METHOD)
                self._update_objects(get_method())

                self._updateMatch = self._tree_itf.connect_to_signal(self._UPDATE_SIGNAL, self._update_object)
                self._removeMatch = self._tree_itf.connect_to_signal(self._REMOVE_SIGNAL, self._remove_object)

                self._connection.add_signal_receiver(self._property_change_handler,
                                                     dbus_interface=self._ATSPI_EVENT_OBJECT_INTERFACE,
                                                     signal_name="property_change",
						     member_keyword="member",
						     sender_keyword="sender",
						     path_keyword="path")
                self._connection.add_signal_receiver(self._children_changed_handler,
                                                     dbus_interface=self._ATSPI_EVENT_OBJECT_INTERFACE,
                                                     signal_name="children_changed",
						     member_keyword="member",
						     sender_keyword="sender",
						     path_keyword="path")

                obj = self._connection.get_object (bus_name, self._CACHE_PATH)
                cache = dbus.Interface (obj, self._CACHE_INTERFACE)

                self.root = cache.GetRoot ()

        def __getitem__(self, key):
                try:
                        name, path = key
                        if name != self_bus_name:
                                raise KeyError ()
                        return self._objects[path]
                except Exception:
                        raise KeyError ()

        def __contains__(self, key):
                try:
                        name, path = key
                        if name != self_bus_name:
                                return False
                        return path in self._objects
                except Exception:
                        return False

        def _update_object (self, data):
                #First element is the object path.
                path = data[0]
                self._objects[path] = _CacheData (data)

        def _update_objects (self, objects):
                for data in objects:
                        self._update_object (data)

        def _remove_object(self, path):
                try:
                        del(self._objects[path])
                except KeyError:
                        pass

	def _property_change_handler (self, app, minor, detail1, detail2, any_data,
				            sender=None, member=None, path=None):
                if (sender, path) in self:
			item = self[(sender, path)]
			if minor == "accessible-name":
				item.name = any_data
			elif minor == "accessible-description":
				item.description = any_data
			elif minor == "accessible-parent":
				item.parent = any_data

	def _children_changed_handler (self, app, minor, detail1, detail2, any_data,
				             sender=None, member=None, path=None):
		if (sender, path) in self:
			item = self[(sender, path)]
			if minor == "add":
				item.children.insert (detail1, any_data)
			elif minor == "remove":
				item.remove (detail1 + 1)

#END----------------------------------------------------------------------------
