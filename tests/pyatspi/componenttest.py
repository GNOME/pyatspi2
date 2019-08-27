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
from pyatspi.Accessibility import Component
from pyatspi.utils import BoundingBox

ATSPI_LAYER_WIDGET = 3
ATSPI_LAYER_MDI = 4
ATSPI_LAYER_WINDOW = 7

extents_expected = [(0,0,30,20), (40,30,30,40), (0,0,70,70)]
sizes_expected = [(30,20), (30,40), (70,70)]
positions_expected = [(0,0), (40,30), (0,0)]
layers_expected = [ATSPI_LAYER_WINDOW, ATSPI_LAYER_WIDGET, ATSPI_LAYER_MDI]
zorders_expected = [-100, 100]

class ComponentTest(_PasyTest):

	__tests__ = ["setup",
		     "test_contains",
		     "test_getAccessibleAtPoint",
		     "test_getExtents",
		     "test_getPosition",
		     "test_getSize",
		     "test_getLayer",
		     "test_getMDIZOrder",
		     "test_grabFocus",
		     "test_registerFocusHandler",
		     "test_deregisterFocusHandler",
		     "test_getAlpha",
		     "teardown",
		     ]

	def __init__(self, bus, path):
		_PasyTest.__init__(self, "Component", False)
		self._bus = bus
		self._path = path

	def setup(self, test):
		self._registry = pyatspi.Registry()
		self._desktop = self._registry.getDesktop(0)
		self._root = pyatspi.findDescendant (self._desktop, lambda x: x.name == "atspi-test-main" and x.getRole() == pyatspi.ROLE_APPLICATION)

	def test_contains(self, test):
		pass

	def test_getAccessibleAtPoint(self, test):
		pass

	def test_getExtents(self, test):
		root = self._root
		one = root.getChildAtIndex(0)
		two = root.getChildAtIndex(1)

		comps = [one.queryComponent(),
			 two.queryComponent(),
			 root.queryComponent(),]
 
		for expected, comp in zip(extents_expected, comps):
			extents = comp.getExtents(0)
			test.assertEqual(extents, BoundingBox(*expected), 
					 "Extents not correct. Expected (%d, %d, %d, %d), Recieved (%d, %d, %d, %d)"
					 % (expected[0], expected[1], expected[2], expected[3], 
						extents[0], extents[1], extents[2], extents[3]))

	def test_getPosition(self, test):
		root = self._root
		one = root.getChildAtIndex(0)
		two = root.getChildAtIndex(1)

		comps = [one.queryComponent(),
			 two.queryComponent(),
			 root.queryComponent(),]
 
		for expected, comp in zip(positions_expected, comps):
			position = comp.getPosition(0)
			test.assertEqual(position, expected, 
					 "Position not correct. Expected (%d, %d) Recieved (%d, %d)"
					 % (expected[0], expected[1], position[0], position[1]))

	def test_getSize(self, test):
		root = self._root
		one = root.getChildAtIndex(0)
		two = root.getChildAtIndex(1)

		comps = [one.queryComponent(),
			 two.queryComponent(),
			 root.queryComponent(),]
 
		for expected, comp in zip(sizes_expected, comps):
			size = comp.getSize()
			test.assertEqual(size, expected, 
					 "Size not correct. Expected (%d, %d) Recieved (%d, %d)"
					 % (expected[0], expected[1], size[0], size[1]))

	def test_getLayer(self, test):
		root = self._root
		one = root.getChildAtIndex(0)
		two = root.getChildAtIndex(1)

		comps = [one.queryComponent(),
			 two.queryComponent(),
			 root.queryComponent(),]
 
		for expected, comp in zip(layers_expected, comps):
			layer = comp.getLayer()
			test.assertEqual(layer, expected, 
					 "Layer not correct. Expected %d, Recieved %d"
					 % (int(layer), int(expected)))

	def test_getMDIZOrder(self, test):
		root = self._root
		one = root.getChildAtIndex(0)
		two = root.getChildAtIndex(1)

		comps = [two.queryComponent(),
			 root.queryComponent(),]
 
		for expected, comp in zip(zorders_expected, comps):
			mdizo = comp.getMDIZOrder()
			test.assertEqual(mdizo, expected, 
					 "ZOrder not correct. Expected %d, Recieved %d"
					 % (expected, mdizo))

	def test_grabFocus(self, test):
		pass

	def test_registerFocusHandler(self, test):
		pass

	def test_deregisterFocusHandler(self, test):
		pass

	def test_getAlpha(self, test):
		pass

	def teardown(self, test):
		pass
