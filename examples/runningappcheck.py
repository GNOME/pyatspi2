#!/usr/bin/python
#
# runningappcheck.py
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
# A pyatspi2 example to demonstrate how to find the number of accessible
# applications currently running on the desktop.

import pyatspi

def on_key_input(event):
	if event.type == pyatspi.KEY_RELEASED_EVENT:
		return False
	if event.event_string=='F4':
		pyatspi.Registry.stop()
		return True
	if event.event_string =='F5':
		name_apps()
		return True
	help_message()

def name_apps():
	desktop = pyatspi.Registry.getDesktop(0)
	print ('there are %s running applications' % (desktop.childCount))
	for app in desktop:
		print app.name

def help_message():
	print('Press F5 to print the running apps.\nPress F4 to exit.')

help_message()
pyatspi.Registry.registerKeystrokeListener(on_key_input, kind=(pyatspi.KEY_PRESSED_EVENT, pyatspi.KEY_RELEASED_EVENT))
pyatspi.Registry.start()
