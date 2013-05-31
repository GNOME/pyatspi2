#!/usr/bin/python
#
# caret.py
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
# This example demonstrates how the pyatspi2 text interface can be used.

import pyatspi

def on_caret_move(event):
    if event.source and event.source.getRole() == pyatspi.ROLE_TERMINAL:
        return

    print_text_at_offset(event.source, event.detail1)

def print_text_at_offset(obj, offset):
    try:
        text = obj.queryText()
    except:
        return
    else:
	char, char_start_offset, char_end_offset = text.getTextAtOffset(offset, pyatspi.TEXT_BOUNDARY_CHAR)
	word, word_start_offset, word_end_offset = text.getTextAtOffset(offset, pyatspi.TEXT_BOUNDARY_WORD_START)
	sentence, sentence_start_offset, sentence_end_offset = text.getTextAtOffset(offset, pyatspi.TEXT_BOUNDARY_SENTENCE_START)
	line, line_start_offset, line_end_offset = text.getTextAtOffset(offset,pyatspi.TEXT_BOUNDARY_LINE_START)
	print("\n\nChar:%s \nWord:%s \nSentence:%s Line:%s " % (char, word, sentence, line))

pyatspi.Registry.registerEventListener(on_caret_move, "object:text-caret-moved")
pyatspi.Registry.start()
