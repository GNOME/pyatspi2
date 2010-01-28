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
import traceback

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

	def _event_dispatch (self):
		while not self._signal_queue.empty():
			(func, args, kwargs) = self._signal_queue.get (False)
			func (*args, **kwargs)
		return False

	def add_signal_receiver (self, func, *args, **kwargs):
		
		def wrapper (*iargs, **ikwargs):
			self._signal_queue.put ((func, iargs, ikwargs))
                	gobject.idle_add(self._event_dispatch)

		return _bus.BusConnection.add_signal_receiver (self, wrapper, *args, **kwargs)

	def get_object (self, name, path):
		return _connection.ProxyObject (self, name, path, introspect=False)
		#return AccessibilityProxy (self, name, path, introspect=False)


class AsyncAccessibilityBus (_AccessibilityBus):
	"""
	Shared instance of the D-Bus bus used for accessibility.

        Events are queued and later delivered from main loop.
        D-Bus calls are made asyncronously.
	"""

	_shared_instance = None
	
	def __new__ (cls):
		if AsyncAccessibilityBus._shared_instance:
			return AsyncAccessibilityBus._shared_instance
		else:
			try:
				AsyncAccessibilityBus._shared_instance = \
                                        _AccessibilityBus.__new__ (cls, _get_accessibility_bus_address(), None)
			except Exception:
				AsyncAccessibilityBus._shared_instance = \
                                        _AccessibilityBus.__new__ (cls, _bus.BusConnection.TYPE_SESSION, None)
			
			return AsyncAccessibilityBus._shared_instance

	def __init__ (self):
		try:
			_AccessibilityBus.__init__ (self, _get_accessibility_bus_address(), None)
		except Exception:
			_AccessibilityBus.__init__ (self, _bus.BusConnection.TYPE_SESSION, None)

class SyncAccessibilityBus (_bus.BusConnection):
	"""
	Shared instance of the D-Bus bus used for accessibility.
	"""

	_shared_instance = None
	
	def __new__ (cls):
		if SyncAccessibilityBus._shared_instance:
			return SyncAccessibilityBus._shared_instance
		else:
			try:
				SyncAccessibilityBus._shared_instance = \
                                        _bus.BusConnection.__new__ (cls, _get_accessibility_bus_address(), None)
			except Exception:
				SyncAccessibilityBus._shared_instance = \
                                        _bus.BusConnection.__new__ (cls, _bus.BusConnection.TYPE_SESSION, None)
			
			return SyncAccessibilityBus._shared_instance

	def __init__ (self):
		try:
			_bus.BusConnection.__init__ (self, _get_accessibility_bus_address(), None)
		except Exception:
			_bus.BusConnection.__init__ (self, _bus.BusConnection.TYPE_SESSION, None)
