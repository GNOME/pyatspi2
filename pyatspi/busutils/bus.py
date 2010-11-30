#Copyright (C) 2009 Codethink Ltd

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

import Queue as _queue

import dbus.bus as _bus
import dbus.connection as _connection

import os as _os

import gobject

from proxy import AccessibilityProxy

import sys

def _get_accessibility_bus_address ():

	from Xlib import display, Xatom

	if "AT_SPI_DISPLAY" in _os.environ.keys():
		dname = _os.environ["AT_SPI_DISPLAY"]
	else:
		dname = None

	if dname:
		d = display.Display(dname)
	else:
		d = display.Display()
	a = d.get_atom ("AT_SPI_BUS")
	s = d.screen().root
	p = s.get_property (a, Xatom.STRING, 0, 100)

	return p.value

class _AccessibilityBus (_bus.BusConnection):
	"""
	The bus used for accessibility

	This bus derives from a normal D-Bus bus but has
	re-entrant signal dispatching.

	Signal callback methods are wrapped so that they deliver to
	a re-entrant queue which is dispatched later in the main loop.

	This class exists because D-Bus signal dispatching is not
	normally re-entrant. The 'dbus_connection_read_write_dispatch'
	method blocks while a message has been borrowed, which is
	normal during signal delivery.
	"""

	def __new__ (cls, address, mainloop):
		return _bus.BusConnection.__new__(cls, address, mainloop)

	def __init__ (self, address, mainloop):
		_bus.BusConnection.__init__(self, address, mainloop)
		self._signal_queue = _queue.Queue ()
                try:
                        test = _AccessibilityBus.eventsFrozen
                except:
                        _AccessibilityBus.eventsFrozen = False
                        _AccessibilityBus.needEventDispatchBuses = []

        def freezeEvents(self):
                _AccessibilityBus.eventsFrozen = True

        def thawEvents(self):
                _AccessibilityBus.eventsFrozen = False
                for bus in _AccessibilityBus.needEventDispatchBuses:
                	gobject.idle_add(bus._event_dispatch)
                        _AccessibilityBus.needEventDispatchBuses = []

	def _event_dispatch (self):
                if _AccessibilityBus.eventsFrozen:
                        if not(self in _AccessibilityBus.needEventDispatchBuses):
                                _AccessibilityBus.needEventDispatchBuses.append(self)
                        return
		while not self._signal_queue.empty():
			(func, args, kwargs) = self._signal_queue.get (False)
			func (*args, **kwargs)
		return False

	def add_signal_receiver (self, func, *args, **kwargs):
		
		def wrapper (*iargs, **ikwargs):
			self._signal_queue.put ((func, iargs, ikwargs))
                        if _AccessibilityBus.eventsFrozen:
                                if not(self in _AccessibilityBus.needEventDispatchBuses):
                                        _AccessibilityBus.needEventDispatchBuses.append(self)
                        else:
                	        gobject.idle_add(self._event_dispatch)

		return _bus.BusConnection.add_signal_receiver (self, wrapper, *args, **kwargs)

	def get_object (self, name, path, introspect=False):
		#return _connection.ProxyObject (self, name, path, introspect=False)
		return AccessibilityProxy (self, name, path, introspect)


class AsyncAccessibilityBus (_AccessibilityBus):
	"""
	Shared instance of the D-Bus bus used for accessibility.

        Events are queued and later delivered from main loop.
        D-Bus calls are made asyncronously.
	"""

	_shared_instances = dict()
	
	def __new__ (cls, registry, address = None):
		try:
			return AsyncAccessibilityBus._shared_instances[address]
		except:
                        pass

                realAddress = address
                if realAddress is None:
                        try:
                                realAddress = _get_accessibility_bus_address()
                        except AttributeError:
                                realAddress = _bus.BusConnection.TYPE_SESSION

                try:
                        AsyncAccessibilityBus._shared_instances[address] = \
                                _AccessibilityBus.__new__ (cls, realAddress, None)
                except:
                        AsyncAccessibilityBus._shared_instances[address] = \
                                _AccessibilityBus.__new__ (cls, _bus.BusConnection.TYPE_SESSION, None)
			
                return AsyncAccessibilityBus._shared_instances[address]

	def __init__ (self, registry, address = None):
		try:
			if self.inited:
				return
		except:
			self.inited = True
                if address is None:
                        try:
                                address = _get_accessibility_bus_address()
                        except AttributeError:
                                address = _bus.BusConnection.TYPE_SESSION
		try:
			_AccessibilityBus.__init__ (self, _get_accessibility_bus_address(), None)
		except AttributeError:
			_AccessibilityBus.__init__ (self, _bus.BusConnection.TYPE_SESSION, None)
                self.registry = registry

class SyncAccessibilityBus (_bus.BusConnection):
	"""
	Shared instance of the D-Bus bus used for accessibility.
	"""

	_shared_instance = None
	
	def __new__ (cls, registry):
		if SyncAccessibilityBus._shared_instance:
			return SyncAccessibilityBus._shared_instance
		else:
			try:
				SyncAccessibilityBus._shared_instance = \
                                        _bus.BusConnection.__new__ (cls, _get_accessibility_bus_address(), None)
			except AttributeError:
				SyncAccessibilityBus._shared_instance = \
                                        _bus.BusConnection.__new__ (cls, _bus.BusConnection.TYPE_SESSION, None)
			
			return SyncAccessibilityBus._shared_instance

	def __init__ (self, registry):
		try:
			if self.inited:
				return
		except:
			self.inited = True
		try:
			_bus.BusConnection.__init__ (self, _get_accessibility_bus_address(), None)
		except AttributeError:
			_bus.BusConnection.__init__ (self, _bus.BusConnection.TYPE_SESSION, None)
                self.registry = registry
