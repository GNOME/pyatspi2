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
from enum import Enum
from accessible import Accessible

from dbus.types import UInt32

__all__ = [
           "Collection",
           "MatchRule",
           "SortOrder",
           "MatchType",
           "TreeTraversalType",
          ]

#------------------------------------------------------------------------------

class MatchType(Enum):
        _enum_lookup = {
                0:'MATCH_INVALID',
                1:'MATCH_ALL',
                2:'MATCH_ANY',
                3:'MATCH_NONE',
                4:'MATCH_EMPTY',
                5:'MATCH_LAST_DEFINED',
        }

class SortOrder(Enum):
        _enum_lookup = {
                0:'SORT_ORDER_INVALID',
                1:'SORT_ORDER_CANONICAL',
                2:'SORT_ORDER_FLOW',
                3:'SORT_ORDER_TAB',
                4:'SORT_ORDER_REVERSE_CANONICAL',
                5:'SORT_ORDER_REVERSE_FLOW',
                6:'SORT_ORDER_REVERSE_TAB',
                7:'SORT_ORDER_LAST_DEFINED',
        }

class TreeTraversalType(Enum):
        _enum_lookup = {
                0:'TREE_RESTRICT_CHILDREN',
                1:'TREE_RESTRICT_SIBLING',
                2:'TREE_INORDER',
                3:'TREE_LAST_DEFINED',
        }

class Collection(Accessible):

        MATCH_ALL = MatchType(1)
        MATCH_ANY = MatchType(2)
        MATCH_EMPTY = MatchType(4)
        MATCH_INVALID = MatchType(0)
        MATCH_LAST_DEFINED = MatchType(5)
        MATCH_NONE = MatchType(3)

        SORT_ORDER_CANONICAL = SortOrder(1)
        SORT_ORDER_FLOW = SortOrder(2)
        SORT_ORDER_INVALID = SortOrder(0)
        SORT_ORDER_LAST_DEFINED = SortOrder(7)
        SORT_ORDER_REVERSE_CANONICAL = SortOrder(4)
        SORT_ORDER_REVERSE_FLOW = SortOrder(5)
        SORT_ORDER_REVERSE_TAB = SortOrder(6)
        SORT_ORDER_TAB = SortOrder(3)

        TREE_INORDER = TreeTraversalType(2)
        TREE_LAST_DEFINED = TreeTraversalType(3)
        TREE_RESTRICT_CHILDREN = TreeTraversalType(0)
        TREE_RESTRICT_SIBLING = TreeTraversalType(1)

        def isAncestorOf(self, object):
                print "isAncestorOf unimplemented"
                return False

        def createMatchRule(self, states, stateMatchType, attributes, attributeMatchType, roles, roleMatchType, interfaces, interfaceMatchType, invert):
                attributes_rule = str.join("\n", attributes)
                roles_rule = [0, 0, 0, 0]
                for role in roles:
                        roles_rule[role/32] |= (1<<(role%32))
                for i in range(0,4):
                        roles_rule[i] = int(roles_rule[i])
                return MatchRule(states, stateMatchType, attributes_rule, attributeMatchType, roles_rule, roleMatchType, interfaces, interfaceMatchType, invert)

        def freeMatchRule(self, rule):
                pass

        def getAccessibles(self, ret):
                for i in range(0, len(ret)):
                        (name, path) = ret[i]
                        if (name == ""):
                                name = self._app_name
                        ret[i] = self.acc_factory (name, path, ATSPI_ACCESSIBLE)
                return ret;

        def getMatches(self, rule, sortby, count, traverse):
                func = self.get_dbus_method("GetMatches", dbus_interface=ATSPI_COLLECTION)
                ret = func(rule, sortby, count, traverse)
                return self.getAccessibles (ret)

        def getMatchesTo(self, current_object, rule, sortby, tree, recurse, count, traverse):
                func = self.get_dbus_method("GetMatchesTo", dbus_interface=ATSPI_COLLECTION)
                ret = func(current_object._acc_path, rule, sortby, tree, recurse, count, traverse)
                return self.getAccessibles (ret)

        def getMatchesFrom(self, current_object, rule, sortby, tree, count, traverse):
                func = self.get_dbus_method("GetMatchesFrom", dbus_interface=ATSPI_COLLECTION)
                ret = func(current_object._acc_path, rule, sortby, tree, count, traverse)
                return self.getAccessibles (ret)

        def getActiveDescendant(self):
                print "getActiveDescendant unimplemented"
                return

class MatchRule(tuple):
        def __new__(cls, states, stateMatchType, attributes, attributeMatchType, roles, roleMatchType, interfaces, interfaceMatchType, invert):
                return tuple.__new__(cls, (states, int(stateMatchType), attributes, int(attributeMatchType), roles, int(roleMatchType), interfaces, int(interfaceMatchType), invert))
        #def __init__(self, states, stateMatchType, attributes, attributeMatchType, roles, roleMatchType, interfaces, interfaceMatchType, invert):
                #tuple.__init__(self, (states, int(stateMatchType), attributes, int(attributeMatchType), roles, int(roleMatchType), interfaces, int(interfaceMatchType), invert))

        def _get_states(self):
                return self[0]
        def _set_states(self, val):
                self[0] = val
        states = property(fget=_get_states, fset=_set_states)
        def _get_stateMatchType(self):
                return self[1]
        def _set_stateMatchType(self, val):
                self[1] = val
        stateMatchType = property(fget=_get_stateMatchType, fset=_set_stateMatchType)
        def _get_attributes(self):
                return self[2]
        def _set_attributes(self, val):
                self[2] = val
        attributes = property(fget=_get_attributes, fset=_set_attributes)
        def _get_attributeMatchType(self):
                return self[3]
        def _set_attributeMatchType(self, val):
                self[3] = val
        attributeMatchType = property(fget=_get_attributeMatchType, fset=_set_attributeMatchType)
        def _get_roles(self):
                return self[4]
        def _set_roles(self, val):
                self[4] = val
        roles = property(fget=_get_roles, fset=_set_roles)
        def _get_roleMatchType(self):
                return self[5]
        def _set_roleMatchType(self, val):
                self[5] = val
        roleMatchType = property(fget=_get_roleMatchType, fset=_set_roleMatchType)
        def _get_interfaces(self):
                return self[6]
        def _set_interfaces(self, val):
                self[6] = val
        interfaces = property(fget=_get_interfaces, fset=_set_interfaces)
        def _get_interfaceMatchType(self):
                return self[7]
        def _set_interfaceMatchType(self, val):
                self[7] = val
        interfaceMatchType = property(fget=_get_interfaceMatchType, fset=_set_interfaceMatchType)
        def _get_invert(self):
                return self[8]
        def _set_invert(self, val):
                self[8] = val
        invert = property(fget=_get_invert, fset=_set_invert)

#END----------------------------------------------------------------------------
