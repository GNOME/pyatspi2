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

__all__ = [
           "ApplicationCache",
           "TestApplicationCache",
           "AccessibleCache"
          ]

#------------------------------------------------------------------------------

class TestApplicationCache(object):

        """
        Test application store, accesses a single application.

        The store object acts as a central class for creating accessible objects.
        It interfaces with the ATSPI registry to keep account of all accessible
        applications. It contains the accessible cache objects from each application.

        @registry:   Each accessible cache object must have a reference to the registry
                     object to send update events.

        @connection: D-Bus connection used to access applications.

        @bus_name:   The test store only accesses one accessible application, this is its
                     D-Bus path.
        """

        def __init__(self, event_dispatcher, connection, bus_name):
                self._application_list = [bus_name]
                self._application_cache = {bus_name:AccessibleCache(event_dispatcher, connection, bus_name)}

        @property
        def application_list (self):
                return self._application_list

        def get_app_root (self, app_name):
                return self._application_cache[app_name].root

        def __call__ (self, app_name, acc_path): 
                """
                Returns the cache tuple for the given application and accessible
                object path. Throws an IndexError if the cache data is not found.
                """
                return self._application_cache[app_name][acc_path]

#------------------------------------------------------------------------------

class ApplicationCache(object):
        """
        Keeps a store of the caches for all accessible applications.
        Updates as new applications are added or removed.

        @event_dispatcher:   Each accessible cache object must have an
                             object to send update events.

        @connection: D-Bus connection used to access applications.
        """

        _APPLICATIONS_ADD = 1
        _APPLICATIONS_REMOVE = 0

        def __init__(self, event_dispatcher, connection):
                self._connection = connection
                self._event_dispatcher = event_dispatcher
                self._factory = None

                self._application_list = []
                self._application_cache = {}

                self._bus_object = connection.get_object("org.freedesktop.DBus",
                                                         "/org/freedesktop/DBus",
                                                         "org.freedektop.DBus")

                this_pid = os.getpid()

                self._regsig = connection.add_signal_receiver(self._update_handler,
                                                              dbus_interface=ATSPI_REGISTRY_INTERFACE,
                                                              signal_name="updateApplications")

                obj = connection.get_object(ATSPI_REGISTRY_NAME,
                                            ATSPI_REGISTRY_PATH,
                                            introspect=False)
                self._app_register = dbus.Interface(obj, ATSPI_REGISTRY_INTERFACE)

                apps = self._app_register.GetApplications()
                for app in apps:
                        that_pid = self._bus_object.GetConnectionUnixProcessID(app)
                        if this_pid != that_pid:
                                self._application_list.append(app)
                        
                for bus_name in self._application_list:
                                self._application_cache[bus_name] = AccessibleCache(self._event_dispatcher,
                                                                                    self._connection,
                                                                                    bus_name)

        def set_factory (self, factory):
                self._factory = factory

        @property
        def application_list (self):
                return self._application_list

        def get_app_root (self, app_name):
                return self._application_cache[app_name].root

        def __call__ (self, app_name, acc_path): 
                """
                Returns the cache tuple for the given application and accessible
                object path. Throws an IndexError if the cache data is not found.
                """
                return self._application_cache[app_name][acc_path]

        def _update_handler (self, update_type, bus_name):
                if update_type == ApplicationCache._APPLICATIONS_ADD:
                        #TODO Check that app does not already exist
                        self._application_list.append(bus_name)
                        self._application_cache[bus_name] = AccessibleCache(self._event_dispatcher,
                                                                            self._connection,
                                                                            bus_name)
                        event = Event(self._factory,
                                      ATSPI_DESKTOP_PATH,
                                      ATSPI_REGISTRY_NAME,
                                      "org.freedesktop.atspi.Event.Object",
                                      "children-changed",
                                      ("add", 0, 0, ""))
                elif update_type == ApplicationCache._APPLICATIONS_REMOVE:
                        #TODO Fail safely if app does not exist
                        self._application_list.remove(bus_name)
                        del(self._application_cache[bus_name])
                        event = Event(self._factory,
                                      ATSPI_DESKTOP_PATH,
                                      ATSPI_REGISTRY_NAME,
                                      "org.freedesktop.atspi.Event.Object",
                                      "children-changed",
                                      ("remove", 0, 0, ""))

                self._event_dispatcher.notifyChildrenChange(event)

        def _refresh(self):
                new = self._app_register.getApplications()
                removed = [item for item in self._application_list if item not in new]
                added   = [item for item in new if item not in self._application_list]
                for item in added:
                        self._update_handler (self._APPLICATIONS_ADD, item)
                for item in removed:
                        self._update_handler (self._APPLICATIONS_REMOVE, item)

                for item in self._application_cache.values():
                        item._refresh()

#------------------------------------------------------------------------------

class _CacheData(object):
        __slots__ = [
                        'path',
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
                        str(self.parent) + '\n' +
                        str(self.children) + '\n' +
                        str(self.interfaces) + '\n' +
                        str(self.name) + '\n' +
                        str(self.role) + '\n' +
                        str(self.description) + '\n' +
                        str(self.state))

        def _update(self, data):
                (self.path,
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

        _PATH = '/org/freedesktop/atspi/tree'
        _INTERFACE = 'org.freedesktop.atspi.Tree'
        _GET_METHOD = 'GetTree'
        _UPDATE_SIGNAL = 'updateAccessible'
        _REMOVE_SIGNAL = 'removeAccessible'

        def __init__(self, event_dispatcher, connection, bus_name):
                """
                Creates a cache.

                connection - DBus connection.
                busName    - Name of DBus connection where cache interface resides.
                """
                self._event_dispatcher = event_dispatcher
                self._connection = connection
                self._bus_name = bus_name

                obj = connection.get_object(bus_name, self._PATH, introspect=False)
                self._tree_itf = dbus.Interface(obj, self._INTERFACE)

                self._objects = {}

                get_method = self._tree_itf.get_dbus_method(self._GET_METHOD)
                self._update_objects(get_method())

                self._updateMatch = self._tree_itf.connect_to_signal(self._UPDATE_SIGNAL, self._update_single)
                self._removeMatch = self._tree_itf.connect_to_signal(self._REMOVE_SIGNAL, self._remove_object)

                self._root = self._tree_itf.GetRoot()

        def set_factory (self, factory):
                pass

        @property
        def application_list (self):
                return [self._bus_name]

        def get_app_root (self, app_name):
                if app_name != self._bus_name:
                        raise KeyError
                return self._root

        def __call__ (self, app_name, acc_path): 
                """
                Returns the cache tuple for the given application and accessible
                object path. Throws an IndexError if the cache data is not found.
                """
                if app_name != self._bus_name:
                        raise KeyError
                return self[acc_path]

        def __getitem__(self, key):
                return self._objects[key]

        def __contains__(self, key):
                return key in self._objects

        def _dispatch_event(self, olddata, newdata):
                if olddata.name != newdata.name:
                        self._event_dispatcher.notifyNameChange(self._bus_name, newdata.path, newdata.name)

                if olddata.description != newdata.description:
                        self._event_dispatcher.notifyDescriptionChange(self._bus_name, newdata.path, newdata.description)

                if olddata.parent != newdata.parent:
                        self._event_dispatcher.notifyParentChange(self._bus_name, newdata.path)

                removed, added = _list_items_added_removed (olddata.children, newdata.children)

                if added:
                        self._event_dispatcher.notifyChildrenChange(self._bus_name, newdata.path, True)

                if removed:
                        self._event_dispatcher.notifyChildrenChange(self._bus_name, newdata.path, False)

        # TODO This should be the other way around. Single is more common than many.
        def _update_single(self, object):
                self._update_objects ([object])

        def _update_objects(self, objects):
                cache_update_objects = []
                for data in objects:
                        #First element is the object path.
                        path = data[0]
                        if path in self._objects:
                                olddata = self._objects[path]
                                newdata = _CacheData(data)
                                cache_update_objects.append((olddata, newdata))
                                self._objects[path] = newdata
                        else:
                                self._objects[path] = _CacheData(data)
                for old, new in cache_update_objects:
                        self._dispatch_event(old, new)

        def _remove_object(self, path):
                # TODO I'm squashing a possible error here
                # I've seen things appear to be deleted twice
                # which needs investigation
                try:
                        del(self._objects[path])
                except KeyError:
                        pass

        def _refresh(self):
                get_method = self._tree_itf.get_dbus_method(self._GET_METHOD)
                self._update_objects(get_method())

        @property
        def root(self):
                return self._root

#END----------------------------------------------------------------------------
