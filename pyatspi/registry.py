#Copyright (C) 2008 Codethink Ltd
#copyright: Copyright (c) 2005, 2007 IBM Corporation

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

#Portions of this code originally licensed and copyright (c) 2005, 2007
#IBM Corporation under the BSD license, available at
#U{http://www.opensource.org/licenses/bsd-license.php}

#authors: Peter Parente, Mark Doffman

#------------------------------------------------------------------------------

from deviceevent import KEY_PRESSED_EVENT as _KEY_PRESSED_EVENT
from deviceevent import KEY_RELEASED_EVENT as _KEY_RELEASED_EVENT

from interfaces import ATSPI_REGISTRY_NAME as _ATSPI_REGISTRY_NAME
from interfaces import ATSPI_DESKTOP_PATH as _ATSPI_DESKTOP_PATH
from interfaces import ATSPI_DESKTOP as _ATSPI_DESKTOP

class Registry(object):
        """
        Wraps the Accessibility.Registry to provide more Pythonic registration for
        events.

        This object should be treated as a singleton, but such treatment is not
        enforced. You can construct another instance of this object and give it a
        reference to the Accessibility.Registry singleton. Doing so is harmless and
        has no point.

        @ivar async: Should event dispatch to local listeners be decoupled from event
                receiving from the registry?
        @type async: boolean
        @ivar reg: Reference to the real, wrapped registry object
        @type reg: Accessibility.Registry
        @ivar dev: Reference to the device controller
        @type dev: Accessibility.DeviceEventController
        @ivar clients: Map of event names to client listeners
        @type clients: dictionary
        @ivar observers: Map of event names to AT-SPI L{_Observer} objects
        @type observers: dictionary
        """
        __shared_state = {}

        def __init__(self, device_event_register, app_event_register, desktop, accessible_factory, main_loop):
                self.__dict__ = self.__shared_state

                self.device_event_register = device_event_register
                self.app_event_register = app_event_register
                self.desktop = desktop
                self.accessible_factory = accessible_factory
                self.main_loop = main_loop

        def __call__(self):
                """
                @return: This instance of the registry
                @rtype: L{Registry}
                """
                return self

        def start(self, async=False, gil=True):
                """
                Enter the main loop to start receiving and dispatching events.

                @param async: Should event dispatch be asynchronous (decoupled) from 
                        event receiving from the AT-SPI registry?
                @type async: boolean
                @param gil: Add an idle callback which releases the Python GIL for a few
                        milliseconds to allow other threads to run? Necessary if other threads
                        will be used in this process.
                        Note - No Longer used.
                @type gil: boolean
                """
                try:
                        self._main_loop.run()
                except KeyboardInterrupt:
                        pass

        def stop(self, *args):
                """
                Quits the main loop.
                """
                self.main_loop.stop()

        def getDesktopCount(self):
                """
                Gets the number of available desktops.

                @return: Number of desktops
                @rtype: integer
                """
                return 1

        def getDesktop(self, i):
                """
                Gets a reference to the i-th desktop.

                @param i: Which desktop to get
                @type i: integer
                @return: Desktop reference
                @rtype: Accessibility.Desktop
                """
                return self.desktop

        def registerEventListener(self, client, *names):
                """
                Registers a new client callback for the given event names. Supports 
                registration for all subevents if only partial event name is specified.
                Do not include a trailing colon.

                For example, 'object' will register for all object events, 
                'object:property-change' will register for all property change events,
                and 'object:property-change:accessible-parent' will register only for the
                parent property change event.

                Registered clients will not be automatically removed when the client dies.
                To ensure the client is properly garbage collected, call 
                L{deregisterEventListener}.

                @param client: Callable to be invoked when the event occurs
                @type client: callable
                @param names: List of full or partial event names
                @type names: list of string
                """
                self._app_event_register.registerEventListener (client, *names)

        def deregisterEventListener(self, client, *names):
                """
                Unregisters an existing client callback for the given event names. Supports 
                unregistration for all subevents if only partial event name is specified.
                Do not include a trailing colon.

                This method must be called to ensure a client registered by
                L{registerEventListener} is properly garbage collected.

                @param client: Client callback to remove
                @type client: callable
                @param names: List of full or partial event names
                @type names: list of string
                @return: Were event names specified for which the given client was not
                        registered?
                @rtype: boolean
                """
                self._app_event_register.deregisterEventListener (client, *names)

        # -------------------------------------------------------------------------------

        def registerKeystrokeListener(self,
                                      client,
                                      key_set=[],
                                      mask=0,
                                      kind=(_KEY_PRESSED_EVENT, _KEY_RELEASED_EVENT),
                                      synchronous=True,
                                      preemptive=True,
                                      global_=False):
                """
                Registers a listener for key stroke events.

                @param client: Callable to be invoked when the event occurs
                @type client: callable
                @param key_set: Set of hardware key codes to stop monitoring. Leave empty
                        to indicate all keys.
                @type key_set: list of integer
                @param mask: When the mask is None, the codes in the key_set will be 
                        monitored only when no modifier is held. When the mask is an 
                        integer, keys in the key_set will be monitored only when the modifiers in
                        the mask are held. When the mask is an iterable over more than one 
                        integer, keys in the key_set will be monitored when any of the modifier
                        combinations in the set are held.
                @type mask: integer, iterable, None
                @param kind: Kind of events to watch, KEY_PRESSED_EVENT or 
                        KEY_RELEASED_EVENT.
                @type kind: list
                @param synchronous: Should the callback notification be synchronous, giving
                        the client the chance to consume the event?
                @type synchronous: boolean
                @param preemptive: Should the callback be allowed to preempt / consume the
                        event?
                @type preemptive: boolean
                @param global_: Should callback occur even if an application not supporting
                        AT-SPI is in the foreground? (requires xevie)
                @type global_: boolean
                """
                self._device_event_register.registerKeystrokeListener (client,
                                                                       key_set,
                                                                       mask,
                                                                       kind,
                                                                       synchronous,
                                                                       preemptive,
                                                                       global_)

        def deregisterKeystrokeListener(self,
                                        client,
                                        key_set=[],
                                        mask=0,
                                        kind=(_KEY_PRESSED_EVENT, _KEY_RELEASED_EVENT)):
                """
                Deregisters a listener for key stroke events.

                @param client: Callable to be invoked when the event occurs
                @type client: callable
                @param key_set: Set of hardware key codes to stop monitoring. Leave empty
                        to indicate all keys.
                @type key_set: list of integer
                @param mask: When the mask is None, the codes in the key_set will be 
                        monitored only when no modifier is held. When the mask is an 
                        integer, keys in the key_set will be monitored only when the modifiers in
                        the mask are held. When the mask is an iterable over more than one 
                        integer, keys in the key_set will be monitored when any of the modifier
                        combinations in the set are held.
                @type mask: integer, iterable, None
                @param kind: Kind of events to stop watching, KEY_PRESSED_EVENT or 
                        KEY_RELEASED_EVENT.
                @type kind: list
                @raise KeyError: When the client isn't already registered for events
                """
                self._device_event_register.deregisterKeystrokeListener (client, key_set, mask, kind)

        # -------------------------------------------------------------------------------

        def pumpQueuedEvents (self):
                """
                No Longer needed all application events are asyncronous.
                """
                pass

        def flushEvents (self):
                """
                No Longer needed all application events are asyncronous.
                """
                pass

        # -------------------------------------------------------------------------------

        def generateKeyboardEvent(self, keycode, keysym, kind):
                """
                Generates a keyboard event. One of the keycode or the keysym parameters
                should be specified and the other should be None. The kind parameter is 
                required and should be one of the KEY_PRESS, KEY_RELEASE, KEY_PRESSRELEASE,
                KEY_SYM, or KEY_STRING.

                @param keycode: Hardware keycode or None
                @type keycode: integer
                @param keysym: Symbolic key string or None
                @type keysym: string
                @param kind: Kind of event to synthesize
                @type kind: integer
                """
                self._device_event_register.generateKeyboardEvent (keycode, keysym, kind)

        def generateMouseEvent(self, x, y, name):
                """
                Generates a mouse event at the given absolute x and y coordinate. The kind
                of event generated is specified by the name. For example, MOUSE_B1P 
                (button 1 press), MOUSE_REL (relative motion), MOUSE_B3D (butten 3 
                double-click).

                @param x: Horizontal coordinate, usually left-hand oriented
                @type x: integer
                @param y: Vertical coordinate, usually left-hand oriented
                @type y: integer
                @param name: Name of the event to generate
                @type name: string
                """
                self._device_event_register.generateMouseEvent (x, y, name)
