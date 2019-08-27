#Copyright (C) 2008 Codethink Ltd

#his program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

from gi.repository import GObject, GLib
from .Events import Events

import traceback

PASY_TEST_NOT_STARTED = 0
PASY_TEST_IN_PROGRESS = 1
PASY_TEST_FAIL = 2
PASY_TEST_WIN = 3

class PasyEvents(Events):
	__events__ = ('finished', )

class PasyTestStep(object):

	def __init__(self, name):
		self.events = PasyEvents()
		self._state = PASY_TEST_NOT_STARTED
		self.failMsg = None

		self._name = name

	def win(self):
		if self._state == PASY_TEST_IN_PROGRESS:
			self._state = PASY_TEST_WIN
			self.events.finished()
	
	def fail(self, msg):
		if self._state == PASY_TEST_IN_PROGRESS:
			self._state = PASY_TEST_FAIL
			self.failMsg = msg
			self.events.finished()

	def assertEqual(self, a, b, msg):
		if a != b:
			self.fail(msg)

	def assertNotEqual(self, a, b, msg):
		if a == b:
			self.fail(msg)

	def run(self):
		self._state = PASY_TEST_IN_PROGRESS
		self.entry()

	def report(self):
		if self._state == PASY_TEST_WIN:
			return "%s - PASSED" % (self._name,)
		elif self._state == PASY_TEST_FAIL:
			return "%s - FAILED - %s" % (self._name, self.failMsg)
		else:
			return "%s - INCOMPLETE" % (self._name,)

	@property
	def state(self):
		return self._state

class PasyTestFunc(PasyTestStep):
	
	def __init__(self, name, func):
		PasyTestStep.__init__(self, name)
		self._func = func

	def entry(self):
		try:
			self._func(self)
		except Exception as e:
			self.fail(e.message)
			traceback.print_exc()
		self.win()

class PasyTest(PasyTestStep):

	__tests__ = []

	def __init__(self, name, cont):
		PasyTestStep.__init__(self, name)

		self._cont = cont
		self._tests = []

		for name in self.__tests__:
			func = getattr(self, name)
			self._addfunc(name, func)

	def _addfunc(self, name, func):
		functest = PasyTestFunc(name, func)
		self._tests.append(functest)

	def entry(self):
		self._iter = self._test_iterator()
		GLib.idle_add(self.idle_handler)

	def idle_handler(self):
		try:
			step = next(self._iter)
			def finished_handler():
				if step.state == PASY_TEST_WIN or self._cont == True:
					GLib.idle_add(self.idle_handler)
				elif step.state == PASY_TEST_FAIL and self._cont == False:
					self.fail("Sub test %s Failed" % step._name)
			step.events.finished += finished_handler
			step.run()
		except StopIteration:
			# No More tests, check for success or fail
			succeeded = True
			for test in self._tests:
				succeeded = succeeded and (test.state == PASY_TEST_WIN)
			if succeeded:
				self.win()
			else:
				self.fail()
		return False

	def _test_iterator(self):
		for test in self._tests:
			yield test

	def report(self):
		if self._state == PASY_TEST_WIN:
			header =  "%s - PASSED" % (self._name,)
		elif self._state == PASY_TEST_FAIL:
			header =  "%s - FAILED" % (self._name,)
		else:
			header =  "%s - INCOMPLETE" %s (self._name,)

		step_messages = []
		for test in self._tests:
			step_messages.append(test.report())

		step_report =  "\n\t".join(step_messages)
		return header + "\n\t" + step_report
