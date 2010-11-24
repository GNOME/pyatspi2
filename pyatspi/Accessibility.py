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

from gi.repository import Atspi

from registry import *
Registry = Registry()

from constants import *
from role import *
from state import *
from utils import *

def Accessible_getitem(self, i):
	if i < 0 or i >= self.get_child_count():
		raise IndexError
	return self.get_child_at_index(i)

def pointToList(point):
	return (point.x, point.y)

def rectToList(rect):
	return (rect.x, rect.y, rect.width, rect.height)

def textAttrToList(ta):
	return (ta.start_offset, ta.end_offset, ta.text)

def rangeToList(r):
	return (r.start_offset, r.end_offset, r.text)

def textRangeToList(r):
	return (r.start_offset, r.end_offset, r.text)

### Accessible ###
Atspi.Accessible.getChildAtIndex = Atspi.Accessible.get_child_at_index
Atspi.Accessible.getAttributes = Atspi.Accessible.get_attributes_as_array
Atspi.Accessible.getApplication = Atspi.Accessible.get_host_application
Atspi.Accessible.__getitem__ = Accessible_getitem
Atspi.Accessible.__len__ = Atspi.Accessible.get_child_count
Atspi.Accessible.__nonzero__ = lambda x: True
Atspi.Accessible.name = property(fget=Atspi.Accessible.get_name)
Atspi.Accessible.getRole = Atspi.Accessible.get_role

### action ###
Atspi.Accessible.queryAction = Atspi.Accessible.get_action
Atspi.Action.doAction = Atspi.Action.do_action
Atspi.Action.getDescription = Atspi.Action.get_description
Atspi.Action.getKeyBinding = Atspi.Action.get_key_binding
Atspi.Action.getName = Atspi.Action.get_name
Atspi.Action.get_nActions = Atspi.Action.get_n_actions

### collection ###
Atspi.Accessible.queryCollection = Atspi.Accessible.get_collection
Atspi.Collection.isAncesterOf = Atspi.Collection.is_ancestor_of
Atspi.Collection.createMatchRule = lambda x, s, smt, a, amt, r, rmt, inv: Atspi.MatchRule.new (s, smt, a, amt, i, imt, r, rmt, inv)
Atspi.Collection.getMatches = Atspi.Collection.get_matches
Atspi.Collection.getMatchesFrom = Atspi.Collection.get_matches_from
Atspi.Collection.getMatchesTo = Atspi.Collection.get_matches_to
Atspi.Collection.getActiveDescendant = Atspi.Collection.get_active_descendant

### component ###
Atspi.Accessible.queryComponent = Atspi.Accessible.get_component
Atspi.Component.getAccessibleAtPoint = Atspi.Component.get_accessible_at_point
Atspi.Component.getAlpha = Atspi.Component.get_alpha
Atspi.Component.getExtents = lambda x,c: rectToList(Atspi.Component.get_extents(x,c))
Atspi.Component.getLayer = Atspi.Component.get_layer
Atspi.Component.getMDIZOrder = Atspi.Component.get_mdi_z_order
Atspi.Component.getPosition = lambda x,p: pointToList(Atspi.Component.get_position(x,p))
Atspi.Component.getSize = lambda x: pointToList(Atspi.Component.get_size(x))
Atspi.Component.grabFocus = Atspi.Component.grab_focus

### document ###
Atspi.Accessible.queryDocument = Atspi.Accessible.get_document
Atspi.Document.getAttributevalue = Atspi.Document.get_attribute_value
Atspi.Document.getAttributes = lambda x: [key + ":" + value for key, value in Atspi.Document.get_attributes (x)]
Atspi.Document.getLocale = Atspi.Document.get_locale

### editable text ###
Atspi.Accessible.queryEditableText = Atspi.Accessible.get_editable_text
Atspi.EditableText.copyText = Atspi.EditableText.copy_text
Atspi.EditableText.cutText = Atspi.EditableText.cut_text
Atspi.EditableText.deleteText = Atspi.EditableText.delete_text
Atspi.EditableText.insertText = Atspi.EditableText.insert_text
Atspi.EditableText.pasteText = Atspi.EditableText.paste_text
Atspi.EditableText.setTextContents = Atspi.EditableText.set_text_contents

### hyperlink ###
Atspi.Hyperlink.getObject = Atspi.Hyperlink.get_object
Atspi.Hyperlink.getURI = Atspi.Hyperlink.get_uri
Atspi.Hyperlink.isValid = Atspi.Hyperlink.is_valid
Atspi.Hyperlink.get_endIndex = Atspi.Hyperlink.get_end_index
Atspi.Hyperlink.get_nAnchors = Atspi.Hyperlink.get_n_anchors
Atspi.Hyperlink.get_startIndex = Atspi.Hyperlink.get_start_index

### hypertext ###
Atspi.Accessible.queryHypertet = Atspi.Accessible.get_hypertext
Atspi.Hypertext.getLink = Atspi.Hypertext.get_link
Atspi.Hypertext.getLinkIndex = Atspi.Hypertext.get_link_index
Atspi.Hypertext.getNLinks = Atspi.Hypertext.get_n_links

### image ###
Atspi.Accessible.queryImage = Atspi.Accessible.get_image
Atspi.Image.getImageExtents = lambda x,c: rectToList(Atspi.Image.get_image_extents(x,c))
Atspi.Image.getImagePosition = lambda x,p: pointToList(Atspi.Image.get_image_position(x,p))
Atspi.Image.getImageSize = lambda x: pointToList(Atspi.Image.get_image_size(x))
Atspi.Image.get_imageDescription = Atspi.Image.get_image_description
Atspi.Image.get_imageLocale = Atspi.Image.get_image_locale

### selection ###
Atspi.Accessible.querySelection = Atspi.Accessible.get_selection
Atspi.Selection.clearSelectio = Atspi.Selection.clear_selection
Atspi.Selection.deselectChild = Atspi.Selection.deselect_child
Atspi.Selection.deselectSelectedChild = Atspi.Selection.deselect_selected_child
Atspi.Selection.getSelectedChild = Atspi.Selection.get_selected_child
Atspi.Selection.isChildSelected = Atspi.Selection.is_child_selected
Atspi.Selection.selectAll = Atspi.Selection.select_all
Atspi.Selection.selectChild = Atspi.Selection.select_child
Atspi.Selection.get_nSelectedChildren = Atspi.Selection.get_n_selected_children

### table ###
Atspi.Accessible.queryTable = Atspi.Accessible.get_table
Atspi.Table.addColumnSelection = Atspi.Table.add_column_selection
Atspi.Table.addRowSelection = Atspi.Table.add_row_selection
Atspi.Table.getAccessibleAt = Atspi.Table.get_accessible_at
Atspi.Table.getColumnAtIndex = Atspi.Table.get_column_at_index
Atspi.Table.getColumnDescription = Atspi.Table.get_column_description
Atspi.Table.getColumnExtentAt = Atspi.Table.get_column_extent_at
Atspi.Table.getColumnHeader = Atspi.Table.get_column_header
Atspi.Table.getIndexAt = Atspi.Table.get_index_at
Atspi.Table.getRowAtIndex = Atspi.Table.get_row_at_index
Atspi.Table.getRowColumnExtents = Atspi.Table.get_row_column_extents_at_index
Atspi.Table.getRowDescription = Atspi.Table.get_row_description
Atspi.Table.getRowExtentAt = Atspi.Table.get_row_extent_at
Atspi.Table.getRowHeader = Atspi.Table.get_row_header
Atspi.Table.getSelectedColumns = Atspi.Table.get_selected_columns
Atspi.Table.getSelectedRows = Atspi.Table.get_selected_rows
Atspi.Table.isColumnSelected = Atspi.Table.is_column_selected
Atspi.Table.isRowSelected = Atspi.Table.is_row_selected
Atspi.Table.isSelected = Atspi.Table.is_selected
Atspi.Table.removeColumnSelection = Atspi.Table.remove_column_selection
Atspi.Table.removeRowSelection = Atspi.Table.remove_row_selection
Atspi.Table.get_nColumns = Atspi.Table.get_n_columns
Atspi.Table.get_nRows = Atspi.Table.get_n_rows
Atspi.Table.get_nSelectedColumns = Atspi.Table.get_n_selected_columns
Atspi.Table.get_nSelectedRows = Atspi.Table.get_n_selected_rows

### text ###
Atspi.Accessible.queryText = Atspi.Accessible.get_text
Atspi.Text.addSelection = Atspi.Text.add_selection
Atspi.Text.getAttributeRun = lambda x,o,i: textAttrToList (Atspi.Text.get_attribute_run (x,o,i))
Atspi.Text.getAttributevalue = Atspi.Text.get_attribute_value
Atspi.Text.getAttributes = lambda x,o: textAttrToList (Atspi.Text.get_attributes (x, o))
Atspi.Text.getBoundedRanges = Atspi.Text.get_bounded_ranges
Atspi.Text.getcharacterAtOffset = Atspi.Text.get_character_at_offset
Atspi.Text.getCharacterExtents = lambda x,c: rectToist(Atspi.Text.get_character_extents(x,c))
Atspi.Text.getDefaultAttributeSet = lambda x: [key + ":" + value for key, value in Atspi.Text.get_default_attribute_set (x)]
Atspi.Text.getDefaultAttributes = lambda x: [key + ":" + value for key, value in Atspi.Text.get_default_attributes (x)]
Atspi.Text.getNSelections = Atspi.Text.get_n_selections
Atspi.Text.getOffsetAtPoint = Atspi.Text.get_offset_at_point
Atspi.Text.getRangeExtents = lambda x,c: rectToist(Atspi.Text.get_range_extents(x,c))
Atspi.Text.getSelection = lambda x,n: rangeToList (Atspi.Text.get_selection (x,n))
Atspi.Text.getText = Atspi.Text.get_text
Atspi.Text.getTextAfterOfset = lambda x,o: textRangeToList(Atspi.Text.get_text_after_offset (x,o))
Atspi.Text.getTextAtOfset = lambda x,o: textRangeToList(Atspi.Text.get_text_at_offset (x,o))
Atspi.Text.getTextBeforeOfset = lambda x,o: textRangeToList(Atspi.Text.get_text_before_offset (x,o))
Atspi.Text.removeSelection = Atspi.Text.remove_selection
Atspi.Text.setCaretOffset = Atspi.Text.set_caret_offset
Atspi.Text.setSelection = Atspi.Text.set_selection
Atspi.Text.get_caretOffset = Atspi.Text.get_caret_offset
Atspi.Text.get_characterCount = Atspi.Text.get_character_count

### value ###
Atspi.Accessible.queryValue = Atspi.Accessible.get_value
Atspi.Value.get_currentValue = Atspi.Value.get_current_value
Atspi.Value.set_currentValue = Atspi.Value.set_current_value
Atspi.Value.get_maximumValue = Atspi.Value.get_maximum_value
Atspi.Value.get_minimumIncrement = Atspi.Value.get_minimum_increment
Atspi.Value.get_minimumValue = Atspi.Value.get_minimum_value

### event ###
Atspi.Event.host_application = lambda x: x.source.host_application
