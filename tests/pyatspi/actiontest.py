#
# Copyright 2008 Codethink Ltd.
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

class ActionTest(_PasyTest):

	__tests__ = ["setup",
		     "test_nActions",
		     "test_getDescription",
		     "test_getName",
		     "test_doAction",
		     "test_getKeyBinding",
		     "teardown",
		     ]

	def __init__(self, bus, path):
		_PasyTest.__init__(self, "Action", False)
		self._bus = bus
		self._path = path

	def setup(self, test):
		self._registry = pyatspi.Registry()
		import time
		self._desktop = self._registry.getDesktop(0)
		print("--desktop len", len(self._desktop))
		for i in self._desktop:
			try:
				print("-- object",i,i.getRole())
			except:
				pass
		self._root = pyatspi.findDescendant (self._desktop, lambda x: x.name == "atspi-test-main" and x.getRole() == pyatspi.ROLE_APPLICATION)
		print("--root", self._root)

	def test_nActions(self, test):
		root = self._root
		root = root.queryAction()
		nact = root.nActions
		test.assertEqual(nact, 10, "nActions expected %d, recieved %d" % (10, nact))

	def test_getName(self, test):
		root = self._root
		root = root.queryAction()
		name = root.getName(0)
		test.assertEqual(name, "First action", "Name expected %s, recieved %s" % ("First action", name))
		name = root.getName(1)
		test.assertEqual(name, "Action", "Name expected %s, recieved %s" % ("Action", name))

	def test_getDescription(self, test):
		root = self._root
		root = root.queryAction()
		description = root.getDescription(0)
		expected = "First action performed"
		test.assertEqual(description, expected, "Description expected %s, recieved %s" % (expected, description))
		description = root.getDescription(1)
		expected = "Description of action"
		test.assertEqual(description, expected, "Description expected %s, recieved %s" % (expected, description))

	def test_doAction(self, test):
		root = self._root
		root = root.queryAction()
		#TODO have event emitted to check action has been performed
		for i in range(0, root.nActions):
			root.doAction(i)

	def test_getKeyBinding(self, test):
		root = self._root
		root = root.queryAction()
		for i in range(0, root.nActions):
			keybinding = root.getKeyBinding(i)
			expected = "%s" % (i,)
			test.assertEqual(keybinding, expected,
					 "Keybinding expected %s, recieved %s" % (expected, keybinding))

	def teardown(self, test):
		pass
