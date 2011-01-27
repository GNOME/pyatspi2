#Copyright (C) 210 Novell, Inc.

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

# Do not replace yourself if you've been imported explicitly by name
# already.
#
import sys
if not sys.modules.has_key('pyatspi_dbus'):
    try:
        import subprocess
        o = subprocess.check_output (("gconftool-2", "--get", "/desktop/gnome/interface/at-spi-corba"))
        useCorba = (o == "true\n")
    except:
        useCorba = False

if useCorba:
    import pyatspi_corba
    sys.modules['pyatspi'] = pyatspi_corba
else:
    __version__ = (1, 9, 0)

    from gi.repository import Atspi

    from Accessibility import *

    #This is a re-creation of the namespace pollution implemented
    #by PyORBit.
    import Accessibility
    sys.modules['Accessibility'] = Accessibility
