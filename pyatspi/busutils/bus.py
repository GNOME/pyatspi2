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

import gobject

from proxy import AccessibilityProxy

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

	def __init__ (self):
                _bus.BusConnection.__init__(self, _bus.BusConnection.TYPE_SESSION, mainloop=None)

		self._signal_queue = _queue.Queue ()

                gobject.idle_add(self._event_dispatch)

	def _event_dispatch (self):
		while not self._signal_queue.empty():
			(func, args, kwargs) = self._signal_queue.get (False)
			func (*args, **kwargs)
		return True

	def add_signal_receiver (self, func, *args, **kwargs):
		
		def wrapper (*iargs, **ikwargs):
			self._signal_queue.put ((func, iargs, ikwargs))

		return _bus.BusConnection.add_signal_receiver (self, wrapper, *args, **kwargs)

	def get_object (self, name, path):
		#return _connection.ProxyObject (self, name, path, introspect=False)
		return AccessibilityProxy (self, name, path, introspect=False)


class AccessibilityBus (_AccessibilityBus):
	"""
	Shared instance of the D-Bus bus used for accessibility.
	"""

	_shared_instance = None
	
	def __new__ (cls):
		if AccessibilityBus._shared_instance:
			return AccessibilityBus._shared_instance
		else:
			AccessibilityBus._shared_instance = _AccessibilityBus.__new__ (cls)
			return AccessibilityBus._shared_instance
