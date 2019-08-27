#
# Copyright 2009 Novell, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.
#

import dbus
from gi.repository import GObject
import os.path

from xml.dom import minidom
import os

from pasytest import PasyTest as _PasyTest

import pyatspi
from pyatspi import StateSet

st = [pyatspi.STATE_MULTI_LINE,
      pyatspi.STATE_MODAL,
      pyatspi.STATE_INDETERMINATE,
      pyatspi.STATE_SUPPORTS_AUTOCOMPLETION,
      pyatspi.STATE_VERTICAL,]

def _createNode(accessible, parentElement):
        e = minidom.Element("accessible")

        e.attributes["name"] = accessible.name
        e.attributes["role"] = str(int(accessible.getRole()))
        e.attributes["description"] = accessible.description

        for i in range(0, accessible.childCount):
                _createNode(accessible.getChildAtIndex(i), e)

        parentElement.appendChild(e)

class AccessibleTest(_PasyTest):

        __tests__ = ["setup",
                     "test_basic",
                     "test_match_any",
                     "test_role",
                     "teardown",
                     ]

        def __init__(self, bus, path):
                _PasyTest.__init__(self, "Collection", False)
                self._bus = bus
                self._path = path


        def setup(self, test):
                self._registry = pyatspi.Registry()
                print(self._path)
                self._desktop = self._registry.getDesktop(0)
                self._root = pyatspi.findDescendant (self._desktop, lambda x: x.name == "atspi-test-main" and x.getRole() == pyatspi.ROLE_WINDOW)

        def assertObjects(self,test,obj,vars,msg):
                test.assertEqual(len(obj), len(vars) // 2, msg + " length")
                for i in range(0, len(vars), 2):
                        test.assertEqual (vars[i], obj[i//2].name, msg + "name" + "#" + str(i//2))
                        test.assertEqual(vars[i+1], obj[i//2].getRole(), msg + " role" + "#" + str(i//2))

        # Used to help add new tests
        def printAsserts(self,obj,msg):
                print("\t\tself.assertObjects(test,ret,(")
                for i in range(0,len(obj)):
                        print("\t\t\t\"" + obj[i].name + "\", " + str(obj[i].getRole()) + ",")
                print("\t\t), \"", msg, "\")")

        def test_basic(self, test):
                collection = self._root.queryCollection()
                stateSet = pyatspi.StateSet()
                rule = collection.createMatchRule (stateSet.raw(),
                        collection.MATCH_NONE,
                [],     # attributes
                        collection.MATCH_NONE,
                [],     # role
                        collection.MATCH_NONE,
                "",     # interfaces
                        collection.MATCH_NONE,
                        False)

                ret = collection.getMatches (rule, collection.SORT_ORDER_CANONICAL, 5, True)
                self.assertObjects(test,ret,(
                        "gnome-settings-daemon", 79 ,
                        "gnome-panel", 79 ,
                        "Bottom Expanded Edge Panel", 25 ,
                        "Top Expanded Edge Panel", 25 ,
                        "nautilus", 79 ,
                ), " 1 ")

                ret = collection.getMatches (rule, collection.SORT_ORDER_REVERSE_CANONICAL, 5, True)
                self.assertObjects(test,ret,(
                        "nautilus", 79,
                        "Top Expanded Edge Panel", 25,
                        "Bottom Expanded Edge Panel", 25,
                        "gnome-panel", 79,
                        "gnome-settings-daemon", 79,
                ), " reverse canonical ")

                obj=ret[2]
                ret = collection.getMatchesTo (obj, rule, collection.SORT_ORDER_REVERSE_CANONICAL, collection.TREE_INORDER, True, 5, True)
                print("--ret:", len(ret))
                self.assertObjects(test,ret,(
                        "gnome-settings-daemon", 79,
                        "gnome-panel", 79,
                ), " getMatchesTo ")
                ret = collection.getMatchesTo (obj, rule, collection.SORT_ORDER_REVERSE_CANONICAL, collection.TREE_INORDER, True, 1, True)
                self.assertObjects(test,ret,(
                        "gnome-panel", 79,
                ), " getMatchesTo w/count=1")
                ret = collection.getMatchesFrom (obj, rule, collection.SORT_ORDER_REVERSE_CANONICAL, collection.TREE_INORDER, 5, True)
                self.assertObjects(test,ret,(
                        "tracker-applet", 79,
                        "metacity", 79,
                        "Desktop", 25,
                        "nautilus", 79,
                        "Top Expanded Edge Panel", 25,
                ), " getMatchesFrom ")
                obj = self._root.getChildAtIndex(1)
                ret = collection.getMatchesFrom (obj, rule, collection.SORT_ORDER_CANONICAL, collection.TREE_RESTRICT_CHILDREN, 5, True)
                self.assertObjects(test,ret,(
                        "Top Expanded Edge Panel", 25,
                ), " Restrict Children ")

        def test_match_any(self, test):
                collection = self._root.queryCollection()
                stateSet = pyatspi.StateSet()
                rule = collection.createMatchRule (stateSet.raw(),
                        collection.MATCH_ANY,
                [],     # attributes
                        collection.MATCH_ANY,
                [],     # role
                        collection.MATCH_ANY,
                "",     # interfaces
                        collection.MATCH_NONE,
                        False)

                ret = collection.getMatches (rule, collection.SORT_ORDER_CANONICAL, 5, True)
                self.assertObjects(test,ret,(
                        "gnome-settings-daemon", 79 ,
                        "gnome-panel", 79 ,
                        "Bottom Expanded Edge Panel", 25 ,
                        "Top Expanded Edge Panel", 25 ,
                        "nautilus", 79 ,
                ), " 1 ")

        def test_role(self, test):
                collection = self._root.queryCollection()
                stateSet = pyatspi.StateSet()

                rule = collection.createMatchRule (stateSet.raw(),
                        collection.MATCH_NONE,
                [],     # attributes
                        collection.MATCH_NONE,
                [pyatspi.ROLE_RADIO_MENU_ITEM],
                        collection.MATCH_ANY,
                "",     # interfaces
                        collection.MATCH_NONE,
                        False)

                ret = collection.getMatches (rule, collection.SORT_ORDER_CANONICAL, 5, True)
                self.assertObjects(test,ret,(
                        "Activity Indicator", 45,
                        "Back", 45,
                        "Forward", 45,
                        "", 45,
                        "Reload", 45,
                ), " role ")

                rule = collection.createMatchRule (stateSet.raw(),
                        collection.MATCH_NONE,
                [],     # attributes
                        collection.MATCH_NONE,
                [pyatspi.ROLE_ENTRY, pyatspi.ROLE_HTML_CONTAINER],
                        collection.MATCH_ANY,
                "",     # interfaces
                        collection.MATCH_NONE,
                        False)

                ret = collection.getMatches (rule, collection.SORT_ORDER_CANONICAL, 5, True)
                self.assertObjects(test,ret,(
                        "gnome-settings-daemon", 79,
                        "gnome-panel", 79,
                        "Bottom Expanded Edge Panel", 25,
                        "Top Expanded Edge Panel", 25,
                        "nautilus", 79,
                        ), " role #2")

        def teardown(self, test):
                pass
