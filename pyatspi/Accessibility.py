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

from settings import get_registry, MAIN_LOOP_GLIB
Registry = get_registry (MAIN_LOOP_GLIB)
del get_registry
del MAIN_LOOP_GLIB

from constants import *
from utils import *

from deviceevent import *
from appevent import *

from accessible import *
from action import *
from application import *
from collection import *
from component import *
from desktop import *
from document import *
from editabletext import *
from hyperlink import *
from hypertext import *
from image import *
from relation import *
from role import *
from selection import *
from state import *
from table import *
from text import *
from value import *
