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
import registry
import string

from interfaces import *
from role import ROLE_DESKTOP_FRAME
import state

from busutils import *


__all__ = [
           "AccessibleCache"
          ]

_ATSPI_CACHE_PATH = '/org/at_spi/cache'
_ATSPI_CACHE_INTERFACE = 'org.a11y.atspi.Cache'
_ATSPI_EVENT_OBJECT_INTERFACE = "org.a11y.atspi.Event.Object"

#------------------------------------------------------------------------------

class _CacheData(object):
        __slots__ = [
                        'reference',
                        'application',
                        'parent',
                        'interfaces',
                        'children',
                        'role',
                        'name',
                        'description',
                        'state',
                        'extraData'
                    ]

        def __init__(self, data):
                self._update(data)

        def __str__(self):
                return (str(self.reference) + '\n' +
                        str(self.application) + '\n' +
                        str(self.parent) + '\n' +
                        str(self.children) + '\n' +
                        str(self.interfaces) + '\n' +
                        str(self.name) + '\n' +
                        str(self.role) + '\n' +
                        str(self.description) + '\n' +
                        str(self.state))

        def _update(self, data):
                (self.reference,
                 self.application,
                 self.parent,
                 self.children,
                 self.interfaces,
                 self.name,
                 self.role,
                 self.description,
                 self.state) = data

#------------------------------------------------------------------------------

class DesktopCacheManager (object):
        """
        Responsible for keeping track of applications as they are added or removed
        from the desktop object.

        Also places a cache item that represents the Desktop object.
        """
 
        def __init__(self, cache):
                bus = SyncAccessibilityBus ()

                self._cache = cache
                self._application_list = {}

                bus.add_signal_receiver(self._children_changed_handler,
                                        #bus_name=ATSPI_REGISTRY_NAME,
                                        #path=ATSPI_ROOT_PATH,
                                        dbus_interface=_ATSPI_EVENT_OBJECT_INTERFACE,
                                        signal_name="ChildrenChanged",
                                        interface_keyword="interface",
                                        member_keyword="member",
                                        sender_keyword="sender",
                                        path_keyword="path")

                obj     = bus.get_object(ATSPI_REGISTRY_NAME, ATSPI_ROOT_PATH, introspect=False)
                desktop = dbus.Interface(obj, ATSPI_ACCESSIBLE)
                apps    = desktop.GetChildren()

                #TODO This is ugly. Perhaps the desktop object should implement the
                #     cache interface also?
                bus_object = bus.get_object("org.freedesktop.DBus", "/org/freedesktop/DBus", introspect=False)
                self._unique_name = bus_object.GetNameOwner (ATSPI_REGISTRY_NAME)
                self._cache[(self._unique_name, ATSPI_ROOT_PATH)] = \
                        _CacheData ( 
                                     ( (self._unique_name, ATSPI_ROOT_PATH),    #Reference
                                       (self._unique_name, ATSPI_NULL_PATH),    #Application
                                       (self._unique_name, ATSPI_NULL_PATH),    #Parent
                                       apps,                                    #Children 
                                       [ATSPI_ACCESSIBLE, ATSPI_COMPONENT],     #Interfaces
                                       "main",                                  #Name
                                       ROLE_DESKTOP_FRAME,                            #Role
                                       "",                                      #Description
                                       [0,0]                                    #State
                                     )
                                   )

                for bus_name, object_path in apps:
                                self._application_list[bus_name] = ApplicationCacheManager (cache, bus_name)

	def _children_changed_handler (self, 
                                       minor, detail1, detail2, any_data, app,
				       interface=None, sender=None, member=None, path=None):
                if interface==_ATSPI_EVENT_OBJECT_INTERFACE and sender == self._unique_name and path == ATSPI_ROOT_PATH:
		        if minor == "add":
                                bus_name, object_path = any_data
                                r = registry.Registry()
                                self._application_list[bus_name] = ApplicationCacheManager(self._cache, bus_name)
		        elif minor == "remove":
                                bus_name, object_path = any_data
                                self._application_list[bus_name].remove_all()
                                del(self._application_list[bus_name])

			item = self._cache[(sender, path)]
			if minor == "add":
				item.children.insert (detail1, any_data)
			elif minor == "remove":
				del (item.children[detail1])

#------------------------------------------------------------------------------

class ApplicationCacheManager (object):
        """
        The application cache manager is responsible for keeping the cache up to date
        with cache items from the given application.
        """


        def __init__(self, cache, bus_name):
                """
                Creates a cache.

                connection - DBus connection.
                busName    - Name of DBus connection where cache interface resides.
                """
                # It is important that this bus is async as registered signals may
                # come from orca itself.
                bus = AsyncAccessibilityBus()

                self._cache = cache
		self._bus_name = bus_name

                cache_obj = bus.get_object (bus_name, _ATSPI_CACHE_PATH, introspect=False)
                cache_itf = dbus.Interface (cache_obj, _ATSPI_CACHE_INTERFACE)
                r = registry.Registry()
                r.freezeEvents()
                self._add_objects(cache_itf.GetItems())
                r.thawEvents()

                self._property_change =  \
                        bus.add_signal_receiver(self._property_change_handler,
                                                bus_name=self._bus_name,
                                                dbus_interface=_ATSPI_EVENT_OBJECT_INTERFACE,
                                                signal_name="PropertyChange",
                                                interface_keyword="interface",
                                                member_keyword="member",
                                                sender_keyword="sender",
                                                path_keyword="path")

                self._children_changed = \
                        bus.add_signal_receiver(self._children_changed_handler,
                                                bus_name=self._bus_name,
                                                dbus_interface=_ATSPI_EVENT_OBJECT_INTERFACE,
                                                signal_name="ChildrenChanged",
                                                interface_keyword="interface",
                                                member_keyword="member",
                                                sender_keyword="sender",
                                                path_keyword="path")

                self._state_changed = \
                        bus.add_signal_receiver(self._state_changed_handler,
                                                bus_name=self._bus_name,
                                                dbus_interface=_ATSPI_EVENT_OBJECT_INTERFACE,
                                                signal_name="StateChanged",
                                                interface_keyword="interface",
                                                member_keyword="member",
                                                sender_keyword="sender",
                                                path_keyword="path")

		self._cache_add = \
                        bus.add_signal_receiver(self._add_object,
                                                bus_name=self._bus_name,
                                                path=_ATSPI_CACHE_PATH,
                                                dbus_interface=_ATSPI_CACHE_INTERFACE,
                                                signal_name="AddAccessible")

		self._cache_remove = \
                        bus.add_signal_receiver(self._remove_object,
                                                bus_name=self._bus_name,
                                                path=_ATSPI_CACHE_PATH,
                                                dbus_interface=_ATSPI_CACHE_INTERFACE,
                                                signal_name="RemoveAccessible")


        def _add_object (self, data):
                #First element is the object reference
                bus_name, object_path = data[0]
                self._cache[(bus_name, object_path)] = _CacheData (data)

        def _remove_object(self, reference):
		bus_name, object_path = reference
                try:
                        del(self._cache[(bus_name, object_path)])
                except KeyError:
                        pass

        def _add_objects (self, objects):
                for data in objects:
                        self._add_object (data)

	def _property_change_handler (self,
                                      minor, detail1, detail2, any_data, app,
				      interface=None, sender=None, member=None, path=None):
                if interface==_ATSPI_EVENT_OBJECT_INTERFACE:
                        if (sender, path) in self._cache:
			        item = self._cache[(sender, path)]
			        if minor == "accessible-name":
				        item.name = any_data
			        elif minor == "accessible-description":
				        item.description = any_data
			        elif minor == "accessible-parent":
				        item.parent = any_data

	def _children_changed_handler (self,
                                       minor, detail1, detail2, any_data, app,
				       interface=None, sender=None, member=None, path=None):
                if interface==_ATSPI_EVENT_OBJECT_INTERFACE:
		        if (sender, path) in self._cache:
			        item = self._cache[(sender, path)]
			        if minor == "add":
				        item.children.insert (detail1, any_data)
			        elif minor == "remove":
				        del (item.children[detail1])

	def _state_changed_handler (self,
                                       minor, detail1, detail2, any_data, app,
				       interface=None, sender=None, member=None, path=None):
                if interface==_ATSPI_EVENT_OBJECT_INTERFACE:
		        if (sender, path) in self._cache:
			        item = self._cache[(sender, path)]
                                val = eval("int(state.STATE_" + string.upper(minor) + ")")
                                high = int(val / 32)
                                low = val % 32
                                if (detail1 == 1):
                                        item.state[high] |= (1 << low)
                                else:
                                        item.state[high] &= ~(1 << low)

        def remove_all (self):
                for bus_name, object_path in self._cache.keys():
                        if bus_name == self._bus_name:
                                del(self._cache[(self._bus_name, object_path)])

#------------------------------------------------------------------------------

class AccessibleCache (dict):

	def __init__ (self, bus_name=None):
		dict.__init__ (self)

                if bus_name:
                        self._manager = ApplicationCacheManager (self, bus_name) 
                else:
                        self._manager = DesktopCacheManager (self)

        def __call__ (self, bus_name, object_path):
                return self[(bus_name, object_path)]

#END----------------------------------------------------------------------------
