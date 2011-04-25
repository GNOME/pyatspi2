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

from gi.repository import Atspi
from gi.repository import GObject
from enum import Enum as _Enum

#------------------------------------------------------------------------------

class StateType(_Enum):
        _enum_lookup = {
                0:'STATE_INVALID',
                1:'STATE_ACTIVE',
                2:'STATE_ARMED',
                3:'STATE_BUSY',
                4:'STATE_CHECKED',
                5:'STATE_COLLAPSED',
                6:'STATE_DEFUNCT',
                7:'STATE_EDITABLE',
                8:'STATE_ENABLED',
                9:'STATE_EXPANDABLE',
                10:'STATE_EXPANDED',
                11:'STATE_FOCUSABLE',
                12:'STATE_FOCUSED',
                13:'STATE_HAS_TOOLTIP',
                14:'STATE_HORIZONTAL',
                15:'STATE_ICONIFIED',
                16:'STATE_MODAL',
                17:'STATE_MULTI_LINE',
                18:'STATE_MULTISELECTABLE',
                19:'STATE_OPAQUE',
                20:'STATE_PRESSED',
                21:'STATE_RESIZABLE',
                22:'STATE_SELECTABLE',
                23:'STATE_SELECTED',
                24:'STATE_SENSITIVE',
                25:'STATE_SHOWING',
                26:'STATE_SINGLE_LINE',
                27:'STATE_STALE',
                28:'STATE_TRANSIENT',
                29:'STATE_VERTICAL',
                30:'STATE_VISIBLE',
                31:'STATE_MANAGES_DESCENDANTS',
                32:'STATE_INDETERMINATE',
                33:'STATE_REQUIRED',
                34:'STATE_TRUNCATED',
                35:'STATE_ANIMATED',
                36:'STATE_INVALID_ENTRY',
                37:'STATE_SUPPORTS_AUTOCOMPLETION',
                38:'STATE_SELECTABLE_TEXT',
                39:'STATE_IS_DEFAULT',
                40:'STATE_VISITED',
                41:'STATE_LAST_DEFINED',
        }

#------------------------------------------------------------------------------

STATE_ACTIVE = StateType(1)
STATE_ANIMATED = StateType(35)
STATE_ARMED = StateType(2)
STATE_BUSY = StateType(3)
STATE_CHECKED = StateType(4)
STATE_COLLAPSED = StateType(5)
STATE_DEFUNCT = StateType(6)
STATE_EDITABLE = StateType(7)
STATE_ENABLED = StateType(8)
STATE_EXPANDABLE = StateType(9)
STATE_EXPANDED = StateType(10)
STATE_FOCUSABLE = StateType(11)
STATE_FOCUSED = StateType(12)
STATE_HAS_TOOLTIP = StateType(13)
STATE_HORIZONTAL = StateType(14)
STATE_ICONIFIED = StateType(15)
STATE_INDETERMINATE = StateType(32)
STATE_INVALID = StateType(0)
STATE_INVALID_ENTRY = StateType(36)
STATE_IS_DEFAULT = StateType(39)
STATE_LAST_DEFINED = StateType(41)
STATE_MANAGES_DESCENDANTS = StateType(31)
STATE_MODAL = StateType(16)
STATE_MULTISELECTABLE = StateType(18)
STATE_MULTI_LINE = StateType(17)
STATE_OPAQUE = StateType(19)
STATE_PRESSED = StateType(20)
STATE_REQUIRED = StateType(33)
STATE_RESIZABLE = StateType(21)
STATE_SELECTABLE = StateType(22)
STATE_SELECTABLE_TEXT = StateType(38)
STATE_SELECTED = StateType(23)
STATE_SENSITIVE = StateType(24)
STATE_SHOWING = StateType(25)
STATE_SINGLE_LINE = StateType(26)
STATE_STALE = StateType(27)
STATE_SUPPORTS_AUTOCOMPLETION = StateType(37)
STATE_TRANSIENT = StateType(28)
STATE_TRUNCATED = StateType(34)
STATE_VERTICAL = StateType(29)
STATE_VISIBLE = StateType(30)
STATE_VISITED = StateType(40)

#------------------------------------------------------------------------------

# Build a dictionary mapping state values to names based on the prefix of the enum constants.

STATE_VALUE_TO_NAME = dict(((value, name[6:].lower().replace('_', ' '))
                            for name, value
                            in globals().items() 
                            if name.startswith('STATE_')))

#------------------------------------------------------------------------------

def _marshal_state_set(bitfield):
        """
        The D-Bus protocol has a stateset object passed
        as a 64bit bitfield. The Bits are passed as two 32bit
        integers.

        This function marshals the D-Bus message into a 
        StateSet object that corresponds to these states.
        """
        (lower, upper) = bitfield

        states = []

        pos = 0
        while (lower):
                if (1L)&lower:
                        states.append(StateType(pos))
                pos+=1
                lower >>= 1

        pos = 32
        while (upper):
                if (1L)&upper:
                        states.append(StateType(pos))
                pos+=1
                upper >>= 1

        return StateSet(*states)

#------------------------------------------------------------------------------

def stateset_init(self, *states):
	GObject.GObject.__init__(self)
	map(self.add, states)

# TODO: Probably remove this hack for 2.2, since BGO#646581 is fixed
def StateSet_getStates(self):
        ret = []
        for i in range(0, 64):
                if (self.states & (1 << i)):
                        ret.append(Atspi.StateType(i))
        return ret

StateSet = Atspi.StateSet
StateSet.getStates = StateSet_getStates
StateSet.isEmpty = StateSet.is_empty
StateSet.raw = lambda x: x
StateSet.unref = lambda x: None
StateSet.__init__ = stateset_init
