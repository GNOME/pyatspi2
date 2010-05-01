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

import string
import gobject
import interfaces
from accessible import BoundingBox
from exceptions import *

from factory import AccessibleFactory
from busutils import *
import registry

__all__ = [
                "Event",
                "EventType",
          ]

#------------------------------------------------------------------------------

class _ELessList(list):
        def __getitem__(self, index):
                try:
                        return list.__getitem__(self, index)
                except IndexError:
                        return None

class EventType(str):
        """
        Wraps the AT-SPI event type string so its components can be accessed 
        individually as klass (can't use the keyword class), major, minor, and detail 
        (klass_major_minor_detail).

        @note: All attributes of an instance of this class should be considered 
                public readable as it is acting a a struct.
        @ivar klass: Most general event type identifier (object, window, mouse, etc.)
        @type klass: string
        @ivar major: Second level event type description
        @type major: string
        @ivar minor: Third level event type description
        @type minor: string
        @ivar detail: Lowest level event type description
        @type detail: string
        @ivar name: Full, unparsed event name as received from AT-SPI
        @type name: string
        @cvar format: Names of the event string components
        @type format: 4-tuple of string
        """

        _SEPARATOR = ':'

        def __init__(self, name):
                """
                Parses the full AT-SPI event name into its components
                (klass:major:minor:detail). If the provided event name is an integer
                instead of a string, then the event is really a device event.

                @param name: Full AT-SPI event name
                @type name: string
                @raise AttributeError: When the given event name is not a valid string 
                """
                stripped = name.strip(self._SEPARATOR)
                separated = stripped.split(self._SEPARATOR, 3)
                self._separated = _ELessList(separated)

                self.klass = self._separated[0]
                self.major = self._separated[1]
                self.minor = self._separated[2]
                self.detail = self._separated[3]

        def is_subtype(self, event_type):
                """
                Determines if the passed event type is a subtype
                of this event.
                """
                if event_type.klass and event_type.klass !=  self.klass:
                        return False
                else:
                        if event_type.major and event_type.major != self.major:
                                return False
                        else:
                                if event_type.minor and event_type.minor != self.minor:
                                        return False
                return True

        @property
        def name(self):
                return str(self)

        @property
        def value(self):
                return str(self)

#------------------------------------------------------------------------------

_interface_to_klass = {
                "org.a11y.atspi.Event.Object":"object",
                "org.a11y.atspi.Event.Window":"window",
                "org.a11y.atspi.Event.Mouse":"mouse",
                "org.a11y.atspi.Event.Keyboard":"keyboard",
                "org.a11y.atspi.Event.Terminal":"terminal",
                "org.a11y.atspi.Event.Document":"document",
                "org.a11y.atspi.Event.Focus":"focus",
                }

_klass_to_interface = {
                "object":"org.a11y.atspi.Event.Object",
                "window":"org.a11y.atspi.Event.Window",
                "mouse":"org.a11y.atspi.Event.Mouse",
                "keyboard":"org.a11y.atspi.Event.Keyboard",
                "terminal":"org.a11y.atspi.Event.Terminal",
                "document":"org.a11y.atspi.Event.Document",
                "focus":"org.a11y.atspi.Event.Focus",
                }

#------------------------------------------------------------------------------

def _major_to_signal_name (name):
        ret = string.upper(name[0])
        for i in range(1,len(name)):
                if (name[i] == '-'):
                        pass
                elif (name[i-1] == '-'):
                        ret += string.upper(name[i])
                else:
                        ret += name[i]
        return ret

def _signal_name_to_major (name):
        ret = string.lower(name[0])
        for i in range(1,len(name)):
                if (name[i] == str.lower(name[i])):
                        ret += name[i]
                else:
                        ret += "-" + string.lower(name[++i])
        return ret

#------------------------------------------------------------------------------

def signal_spec_to_event_type (interface, name, minor):
        """
        Converts an AT-SPI D-Bus signal specification into a Corba AT-SPI
        event type.
        """
        klass = _interface_to_klass[interface]
        major = _signal_name_to_major (name)

        if klass == "focus":
                return EventType ("focus:")

        event_string = klass + ':' + major
        if minor:
                event_string += ":" + minor
        return EventType (event_string)

def event_type_to_signal_reciever(bus, factory, event_handler, event_type):
        """
        Converts a Corba AT-SPI event type to the correct D-Bus AT-SPI signal
        reciever.
        """
        kwargs = {
                        'sender_keyword':'sender',
                        'interface_keyword':'interface',
                        'member_keyword':'member',
                        'path_keyword':'path',
                 }
        if event_type.klass:
                kwargs['dbus_interface'] = _klass_to_interface[event_type.klass]
        if event_type.major:
                kwargs['signal_name'] = _major_to_signal_name (event_type.major)
        if event_type.minor:
                kwargs['arg0'] = event_type.minor

        def handler_wrapper(minor,
                            detail1,
                            detail2,
                            any_data,
                            source_application,
                            sender=None,
                            interface=None,
                            member=None,
                            path=None):

                # Convert the event type
                type = signal_spec_to_event_type (interface, member, minor)

                # Marshal the 'any_data' to correct class / structure
                if   type.is_subtype (EventType ("object:bounds-changed")):
                        any_data = BoundingBox(*any_data)
                elif (type.is_subtype (EventType ("object:children-changed")) or
                      type.is_subtype (EventType ("object:property-change:accessible-parent")) or
                      type.is_subtype (EventType ("object:active-descendant-changed"))):
                        data_name, data_path = any_data;
                        any_data = factory (data_name, data_path, interfaces.ATSPI_ACCESSIBLE)

                # Create the source application
                source_app_name, source_app_path = source_application
                source_application = factory (source_app_name, source_app_path, interfaces.ATSPI_APPLICATION)

                # Create the source
                source_name = sender
                source_path = path
                if (path == interfaces.ATSPI_ROOT_PATH):
                        source_itf = interfaces.ATSPI_APPLICATION
                else:
                        source_itf = interfaces.ATSPI_ACCESSIBLE
                source = factory (source_name, source_path, source_itf)

                event = Event (type,
                               detail1,
                               detail2,
                               any_data,
                               source_application,
                               source)
                depth = gobject.main_depth()
                r = registry.Registry()
                if (r.asyncInternal() and depth > 1):
                    r.enqueueEvent(event_handler, event)
                else:
                        return event_handler(event)

        return bus.add_signal_receiver(handler_wrapper, **kwargs)

#------------------------------------------------------------------------------

class Event(object):
        """
        Wraps an AT-SPI event with a more Pythonic interface managing exceptions,
        the differences in any_data across versions, and the reference counting of
        accessibles provided with the event.

        @note: All unmarked attributes of this class should be considered public
                readable and writable as the class is acting as a record object.

        @ivar type: The type of the AT-SPI event
        @type type: L{EventType}
        @ivar detail1: First AT-SPI event parameter
        @type detail1: integer
        @ivar detail2: Second AT-SPI event parameter
        @type detail2: integer
        @ivar any_data: Extra AT-SPI data payload
        @type any_data: object
        @ivar host_application: Application owning the event source
        @type host_application: Tuple (Name, Path)
        @ivar source: Source of the event
        @type source: Accessibility.Accessible
        """
        def __init__(self,
                     type_slash_event=None,
                     detail1=None,
                     detail2=None,
                     any_data=None,
                     host_application=None,
                     source=None):

                if detail1 == None:
                        #This alternative init is provided for compatibility with the old API.
                        #The old API apparently allowed the event to be delivered as a class with
                        #named parameters. (Something like a copy constructor)
                        #Old API used in orca - focus_tracking_presenter.py line 1106
                        event = type_slash_event

                        self.type = event.type
                        self.detail1 = event.detail1
                        self.detail2 = event.detail2
                        self.any_data = event.any_data
                        self.source = event.source
                        self.application = event.source
                else:
                        type = type_slash_event

                        self.type = type
                        self.detail1 = detail1
                        self.detail2 = detail2
                        self.any_data = any_data
                        self.source = source
                        self.host_application = host_application

        @property
        def source_name(self):
                return source.name

        @property
        def source_role(self):
                return source.getRole()

        def __str__(self):
                """
                Builds a human readable representation of the event including event type,
                parameters, and source info.

                @return: Event description
                @rtype: string
                """
                return '%s(%s, %s, %s)\n\tsource: %s\n\thost_application: %s' % \
                                         (self.type, self.detail1, self.detail2, self.any_data,
                                                self.source, self.host_application)

#------------------------------------------------------------------------------

class _ApplicationEventRegister (object):

        def __init__ (self, factory):
                self._bus = AsyncAccessibilityBus ()
                self._factory = factory

                self._event_listeners = {}

        def registerEventListener (self, client, *names):
                try:
                        registered = self._event_listeners[client]
                except KeyError:
                        registered = []
                        self._event_listeners[client] = registered

                for name in names:
                        new_type = EventType(name)
                        registered.append((new_type.name,
                                           event_type_to_signal_reciever(self._bus, self._factory, client, new_type)))

        def deregisterEventListener(self, client, *names):
                try:
                        registered = self._event_listeners[client]
                except KeyError:
                        # Presumably if were trying to deregister a client with
                        # no names then the return type is always true.
                        return True

                missing = False

                for name in names:
                        remove_type = EventType(name)
                        copy = registered[:]
                        for i in range (0, len(copy)):
                                type_name, signal_match = copy[i]
                                registered_type = EventType(type_name)

                                if remove_type.is_subtype(registered_type):
                                        signal_match.remove()
                                        del(registered[i])
                                else:
                                        missing = True

                if registered == []:
                        del(self._event_listeners[client])

                return missing

#------------------------------------------------------------------------------

class _NullApplicationEventRegister (object):

        def registerEventListener(self, client, *names):
                pass

        def deregisterEventListener(self, client, *names):
                return FALSE

#END----------------------------------------------------------------------------
