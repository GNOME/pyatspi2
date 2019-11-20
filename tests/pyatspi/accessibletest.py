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
from pyatspi import StateSet

st = [pyatspi.STATE_MULTI_LINE,
      pyatspi.STATE_MODAL,
      pyatspi.STATE_INDETERMINATE,
      pyatspi.STATE_SUPPORTS_AUTOCOMPLETION,
      pyatspi.STATE_VERTICAL,]

def _createNode(doc, accessible, parentElement):
	e = minidom.Element("accessible")

	nameA = doc.createAttribute('name')
	roleA = doc.createAttribute('role')
	descA = doc.createAttribute('description')
	e.setAttributeNode(nameA)
	e.setAttributeNode(roleA)
	e.setAttributeNode(descA)
	e.setAttribute("name", accessible.name)
	e.setAttribute("role", str(int(accessible.getRole())))
	e.setAttribute("description", accessible.description)

	for i in range(0, accessible.childCount):
		_createNode(doc, accessible.getChildAtIndex(i), e)

	parentElement.appendChild(e)

class AccessibleTest(_PasyTest):

	__tests__ = ["setup",
		     "test_name",
		     "test_getChildAtIndex",
		     "test_isEqual",
		     "test_getApplication",
		     "test_getAttributes",
		     "test_parent",
		     "test_getIndexInParent",
		     "test_getLocalizedRoleName",
		     "test_getRelationSet",
		     "test_getRole",
		     "test_getRoleName",
		     "test_getState",
		     "test_childCount",
		     "test_description",
		     "test_tree",
		     "test_null_interface",
		     "teardown",
		     ]

	def __init__(self, bus, path):
		_PasyTest.__init__(self, "Accessible", False)
		self._bus = bus
		self._path = path

	def setup(self, test):
		self._registry = pyatspi.Registry()
		self._desktop = self._registry.getDesktop(0)
		self._root = pyatspi.findDescendant (self._desktop, lambda x: x.name == "atspi-test-main" and x.getRole() == pyatspi.ROLE_WINDOW)

	def test_name(self, test):
		root = self._root
		test.assertEqual(root.name, "atspi-test-main", "Expected name - \"main\". Recieved - \"%s\"" % (root.name,))

	def test_getChildAtIndex(self, test):
		root = self._root
		a = root.getChildAtIndex(0)
		test.assertEqual(a.name, "gnome-settings-daemon",
					 "Expected name - \"gnome-settings-daemon\". Recieved - \"%s\"" % (a.name,))
		b = root.getChildAtIndex(1)
		test.assertEqual(b.name, "gnome-panel",
					 "Expected name - \"gnome-panel\". Recieved - \"%s\"" % (b.name,))
		c = root.getChildAtIndex(2)
		test.assertEqual(c.name, "nautilus",
					 "Expected name - \"nautilus\". Recieved - \"%s\"" % (c.name,))
		
	def test_isEqual(self, test):
		root = self._root

		a = root.getChildAtIndex(1)
		if not a.isEqual(a):
			test.fail("Same accessible found unequal to self")

		b = root.getChildAtIndex(1)
		if not a.isEqual(b):
			test.fail("Similar accessibles found unequal")
		if not b.isEqual(a):
			test.fail("Similar accessibles found unequal")

		c = root.getChildAtIndex(2)
		if c.isEqual(a):
			test.fail("Different accessibles found equal")
		if a.isEqual(c):
			test.fail("Different accessibles found equal")

	def test_getApplication(self, test):
		root = self._root
		application = root.getApplication()
		if not root.isEqual(application):
			test.fail("Root accessible does not provide itself as its Application")

		a = root.getChildAtIndex(1)
		application = a.getApplication()
		if not root.isEqual(application):
			test.fail("Child accessible does not provide the root as its Application")


	def test_getAttributes(self, test):
		root = self._root
		attr = root.getAttributes()
		res = ["foo:bar", "baz:qux", "quux:corge"]
		attr.sort()
		res.sort()
		test.assertEqual(attr, res, "Attributes expected %s, recieved %s" % (res, attr))

	def test_parent(self, test):
		root = self._root

		a = root.getChildAtIndex(1)
		pa = a.parent
		if not root.isEqual(pa):
			test.fail("Child does not correctly report its parent")

	def test_getIndexInParent(self, test):
		root = self._root

		for i in range(0, root.childCount):
			child = root.getChildAtIndex(i)
			test.assertEqual(i, child.getIndexInParent(), "Childs index in parent reported incorrectly")

	def test_getLocalizedRoleName(self, test):
		root = self._root

		ans = "window"
		res = root.getLocalizedRoleName()
		test.assertEqual(ans, res,
				 "Expected LocalizedRoleName - \"%s\". Recieved - \"%s\"" % (ans, res,))

		a = root.getChildAtIndex(1)
		a = a.getChildAtIndex(0)
		ans = "html container"
		res = a.getLocalizedRoleName()
		test.assertEqual(ans, res,
				 "Expected LocalizedRoleName - \"%s\". Recieved - \"%s\"" % (ans, res,))

	def test_getRelationSet(self, test):
		root = self._root
		# Complete test of Relation interface is separate
		rset = root.getRelationSet()

	def test_getRole(self, test):
		root = self._root
		test.assertEqual(root.getRole(), 69,
				 "Expected role - \"69\". Recieved - \"%d\"" % (int(root.getRole()),))

	def test_getRoleName(self, test):
		root = self._root

		ans = "window"
		res = root.getRoleName()
		test.assertEqual(ans, res,
				 "Expected roleName - \"%s\". Recieved - \"%s\"" % (ans, res,))

		a = root.getChildAtIndex(1)
		a = a.getChildAtIndex(0)
		ans = "html container"
		res = a.getRoleName()
		test.assertEqual(ans, res,
				 "Expected roleName - \"%s\". Recieved - \"%s\"" % (ans, res,))

	def test_getState(self, test):
		root = self._root
		state = root.getState()
		res = StateSet(*st)
		if not res.equals(state):
			test.fail("States not reported correctly")

	def test_childCount(self, test):
		root = self._root
		test.assertEqual(root.childCount, 11,
				 "Expected role - \"11\". Recieved - \"%d\"" % (root.childCount,))

	def test_description(self, test):
		root = self._root
		description = "The main accessible object, root of the accessible tree"
		test.assertEqual(root.description, description,
				 "Expected description - \"%s\". Recieved - \"%s\"" % (description, root.description,))

	def test_tree(self, test):
		"""
		This is a mild stress test for the 
		methods:

		getChildAtIndex
		
		And the attributes:

		name
		description

		It checks a tree of these values is correctly
		passed from Application to AT.
		"""
		root = self._root

		doc = minidom.Document()
		_createNode(doc, root, doc)
		answer = doc.toprettyxml()


		correct = os.path.join(os.environ["TEST_DATA_DIRECTORY"],
					"accessible-test-results.xml")
		file = open(correct)
		cstring = file.read()

		correct2 = os.path.join(os.environ["TEST_DATA_DIRECTORY"],
					"accessible-test-results-stable.xml")
		file = open(correct2)
		cstring2 = file.read()
		
		if answer != cstring and \
		   answer != cstring2:
		    test.fail("Object tree not passed correctly")

	def test_null_interface(self, test):
		root = self._root
		try:
			text = root.queryText()
		except NotImplementedError:
			return
		test.fail ("Should throw NotImplementedError")

	def teardown(self, test):
		pass
