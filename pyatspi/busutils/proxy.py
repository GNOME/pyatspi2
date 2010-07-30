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

import dbus.connection as _connection
import gobject
import threading

import Queue

class _MainLoopPool (Queue.Queue):
	_RE_ENTRANCY_LIMIT = 100
	
	def __init__ (self):
		Queue.Queue.__init__(self)
		for i in range (0, _MainLoopPool._RE_ENTRANCY_LIMIT):
			self.put(gobject.MainLoop())

class AccessibilityProxy (_connection.ProxyObject):
	"""
	Wrapper for the D-Bus Proxy object that makes re-entrant D-Bus calls.

	This class enforces only one level of re-entrancy. This should be all
	that is required as requests for a11y information about the current
	process should not make further D-Bus calls.
	"""

	# We need a pool here as we end up creating so many main loops that we
	# run out of file descriptors!
	_main_loop_pool = _MainLoopPool ()

        class DBusMethodCallbackData (object):
                def __init__ (self, proxy):
			# Will raise the Empty exception if we have hit
			# The re-entrancy limit
                        if proxy._bus.registry.has_implementations == False or proxy._bus.registry.started == False or threading.currentThread() == proxy._bus.registry.thread:
			        self.event = None
			        self.loop  = AccessibilityProxy._main_loop_pool.get_nowait ()
                        else:
			        self.event = threading.Event()
			        self.loop  = None
                        self.error = None
                        self.args  = None
        
        def get_dbus_method (self, *args, **kwargs):
                method = _connection.ProxyObject.get_dbus_method (self, *args, **kwargs)

                def dbus_method_func (*iargs, **ikwargs):

			#depth = gobject.main_depth()
			#print ("\t" * depth) + "---------------"
			#print ("\t" * depth) + "Pre-recurse"
			#print ("\t" * depth) + "Args=" + str(args)
			#print ("\t" * depth) + "Depth=" + str(gobject.main_depth())
			#print

                        self._bus.registry.acquireLock()
                        data = AccessibilityProxy.DBusMethodCallbackData(self)

                        def method_error_callback (e):
                                data.error = e
				def main_quit ():
					data.loop.quit()
					return False
                                if data.event is not None:
                                        data.event.set()
                                else:
				        gobject.idle_add (main_quit)

                        def method_reply_callback (*jargs):

				#depth = gobject.main_depth()
				#print ("\t" * depth) + "Callback"
				#print ("\t" * depth) + "Args=" + str(args)
				#print ("\t" * depth) + "Depth=" + str(gobject.main_depth())
				#print

                                data.args = jargs
				def main_quit ():
					data.loop.quit()
					return False

                                if data.event is not None:
                                        data.event.set()
                                else:
				        gobject.idle_add (main_quit)

                        method (reply_handler=method_reply_callback,
                                error_handler=method_error_callback,
                                *iargs,
                                **ikwargs)

			self._bus.freezeEvents()
                        if data.event is not None:
                                data.event.wait()
                        else:
			        data.loop.run ()
			AccessibilityProxy._main_loop_pool.put_nowait (data.loop)
			self._bus.thawEvents()
                        self._bus.registry.releaseLock()

			#depth = gobject.main_depth()
			#print ("\t" * depth) + "Post-recurse"
			#print ("\t" * depth) + "Depth=" + str(gobject.main_depth())
			#print ("\t" * depth) + "---------------"
			#print

                        if data.error:
                                raise data.error

			if data.args == None:
				raise Exception ("Return arguments not set")

                        if len (data.args) == 0:
                                return None
                        elif len (data.args) == 1:
                                return data.args[0]
                        else:
                                return data.args


                return dbus_method_func
