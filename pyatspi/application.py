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

from interfaces import *
from accessible import Accessible

import dbus

__all__ = [
                  "Application",
          ]

#------------------------------------------------------------------------------

class Application(Accessible):
        """
        An interface identifying an object which is the root of the user
        interface Accessible hierarchy associated with a running application.
        Children of Application are typically, but not exclusively, top-level
        windows.
        """

        def getLocale(self, locale_type):
                """
                Gets the locale in which the application is currently operating.
                For the current message locale, use lctype LOCALE_TYPE_MESSAGES.
                @param : lctype
                The LocaleType for which the locale is queried. 
                @return a string compliant with the POSIX standard for locale
                description.
                """
                func = self.get_dbus_method("GetLocale", dbus_interface=ATSPI_APPLICATION)
                return func(local_type)

        def get_id(self):
                return dbus.Int32(self._pgetter(ATSPI_APPLICATION, "Id"))
        _idDoc = \
                """
                The application instance's unique ID as assigned by the registry.
                """
        id = property(fget=get_id, doc=_idDoc)

        def get_toolkitName(self):
                return dbus.String(self._pgetter(ATSPI_APPLICATION, "ToolkitName"))
        _toolkitNameDoc = \
                """
                A string indicating the type of user interface toolkit which
                is used by the application.
                """
        toolkitName = property(fget=get_toolkitName, doc=_toolkitNameDoc)

        def get_version(self):
                return dbus.String(self._pgetter(ATSPI_APPLICATION, "Version"))
        _versionDoc = \
                """
                A string indicating the version number of the application's accessibility
                bridge implementation.
                """
        version = property(fget=get_version, doc=_versionDoc)

#END----------------------------------------------------------------------------
