#!/usr/bin/python
#
# keypress.py
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.
#
# An pyatspi2 example to demonstate a client listener for
# Keypresses and releases in pyatspi2

import pyatspi

# Callback to print the active window on key press amd filter out the key release
def on_key_input(event):

	if event.type == pyatspi.KEY_RELEASED_EVENT:
		return False
	if event.event_string=='F4':
		pyatspi.Registry.stop()
		return True
	if event.event_string =='F3':
		print_tree(0, active_window())
		return True
	help_message()

def active_window():
	desktop = pyatspi.Registry.getDesktop(0)
	for app in desktop:
		for window in app:
			if window.getState().contains(pyatspi.STATE_ACTIVE):
				return window

# Print hierarchy tree.
def print_tree(level,root):
	print ('%s-> %s' % (' ' * level, root))
	for tree in root:
		print_tree(level+1, tree)

def help_message():
	print('Press F3 to print the accessible hierarchy for the active window.\nPress F4 to exit.')

help_message()
pyatspi.Registry.registerKeystrokeListener(on_key_input, kind=(pyatspi.KEY_PRESSED_EVENT, pyatspi.KEY_RELEASED_EVENT))
pyatspi.Registry.start()
