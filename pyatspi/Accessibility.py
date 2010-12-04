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
        len=self.get_child_count()
        if i < 0:
                i = len + i
	if i < 0 or i >= len:
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
	return (r.text, r.start_offset, r.end_offset)

# TODO: Figure out how to override Atspi.Rect constructor and remove this class
class BoundingBox(list):
        def __new__(cls, x, y, width, height):
                return list.__new__(cls, (x, y, width, height))
        def __init__(self, x, y, width, height):
                list.__init__(self, (x, y, width, height))

        def __str__(self):
                return ("(%d, %d, %d, %d)" % (self.x, self.y, self.width, self.height))

        def _get_x(self):
                return self[0]
        def _set_x(self, val):
                self[0] = val
        x = property(fget=_get_x, fset=_set_x)
        def _get_y(self):
                return self[1]
        def _set_y(self, val):
                self[1] = val
        y = property(fget=_get_y, fset=_set_y)
        def _get_width(self):
                return self[2]
        def _set_width(self, val):
                self[2] = val
        width = property(fget=_get_width, fset=_set_width)
        def _get_height(self):
                return self[3]
        def _set_height(self, val):
                self[3] = val
        height = property(fget=_get_height, fset=_set_height)

def getBoundingBox(rect):
	return BoundingBox (rect.x, rect.y, rect.width, rect.height)

def attributeListToHash(list):
	ret = dict()
	for key, val in list:
		ret[key] = val
	return ret

def getInterface(func, obj):
	ret = func(obj)
	if ret:
		return ret
	raise NotImplementedError

### Accessible ###
Accessible = Atspi.Accessible
Atspi.Accessible.getChildAtIndex = Atspi.Accessible.get_child_at_index
Atspi.Accessible.getAttributes = Atspi.Accessible.get_attributes_as_array
Atspi.Accessible.getApplication = Atspi.Accessible.get_application
Atspi.Accessible.__getitem__ = Accessible_getitem
Atspi.Accessible.__len__ = Atspi.Accessible.get_child_count
Atspi.Accessible.__nonzero__ = lambda x: True
Atspi.Accessible.childCount = property(fget=Atspi.Accessible.get_child_count)
Atspi.Accessible.getIndexInParent = Atspi.Accessible.get_index_in_parent
Atspi.Accessible.getLocalizedRoleName = Atspi.Accessible.get_localized_role_name
Atspi.Accessible.getRelationSet = Atspi.Accessible.get_relation_set
Atspi.Accessible.getRole = Atspi.Accessible.get_role
Atspi.Accessible.getRoleName = Atspi.Accessible.get_role_name
Atspi.Accessible.getState = Atspi.Accessible.get_state_set
Atspi.Accessible.name = property(fget=Atspi.Accessible.get_name)
Atspi.Accessible.isEqual = lambda a,b: a == b
Atspi.Accessible.parent = property(fget=Atspi.Accessible.get_parent)

Atspi.Accessible.toolkitName = property(fget=Atspi.Accessible.get_toolkit_name)
Atspi.Accessible.toolkitVersion = property(fget=Atspi.Accessible.get_toolkit_version)

### action ###
Action = Atspi.Action
Atspi.Accessible.queryAction = lambda x: getInterface(Atspi.Accessible.get_action, x)
Atspi.Action.doAction = Atspi.Action.do_action
Atspi.Action.getDescription = Atspi.Action.get_description
Atspi.Action.getKeyBinding = Atspi.Action.get_key_binding
Atspi.Action.getName = Atspi.Action.get_name
Atspi.Action.nActions = property(fget=Atspi.Action.get_n_actions)

### collection ###
Collection = Atspi.Collection
Atspi.Accessible.queryCollection = lambda x: getInterface(Atspi.Accessible.get_collection, x)
Atspi.Collection.isAncesterOf = Atspi.Collection.is_ancestor_of
Atspi.Collection.createMatchRule = lambda x, s, smt, a, amt, r, rmt, i, imt, inv: Atspi.MatchRule.new (s, smt, attributeListToHash(a), amt, r, rmt, i, imt, inv)
Atspi.Collection.getMatches = Atspi.Collection.get_matches
Atspi.Collection.getMatchesFrom = Atspi.Collection.get_matches_from
Atspi.Collection.getMatchesTo = Atspi.Collection.get_matches_to
Atspi.Collection.getActiveDescendant = Atspi.Collection.get_active_descendant

Atspi.Collection.MATCH_INVALID = Atspi.CollectionMatchType.INVALID
Atspi.Collection.MATCH_ALL = Atspi.CollectionMatchType.ALL
Atspi.Collection.MATCH_ANY = Atspi.CollectionMatchType.ANY
Atspi.Collection.MATCH_NONE = Atspi.CollectionMatchType.NONE
Atspi.Collection.MATCH_EMPTY = Atspi.CollectionMatchType.EMPTY

Atspi.Collection.SORT_ORDER_INVALID = Atspi.CollectionSortOrder.INVALID
Atspi.Collection.SORT_ORDER_CANONICAL = Atspi.CollectionSortOrder.CANONICAL
Atspi.Collection.SORT_ORDER_FLOWAL = Atspi.CollectionSortOrder.FLOW
Atspi.Collection.SORT_ORDER_TAB = Atspi.CollectionSortOrder.TAB
Atspi.Collection.SORT_ORDER_REVERSE_CANONICAL = Atspi.CollectionSortOrder.REVERSE_CANONICAL
Atspi.Collection.SORT_ORDER_REVERSE_FLOW = Atspi.CollectionSortOrder.REVERSE_FLOW
Atspi.Collection.SORT_ORDER_REVERSE_TAB = Atspi.CollectionSortOrder.REVERSE_TAB

Atspi.Collection.TREE_RESTRICT_CHILDREN = Atspi.CollectionTreeTraversalType.RESTRICT_CHILDREN
Atspi.Collection.TREE_RESTRICT_SIBLING = Atspi.CollectionTreeTraversalType.RESTRICT_SIBLING
Atspi.Collection.TREE_INORDER = Atspi.CollectionTreeTraversalType.INORDER

### component ###
Component = Atspi.Component
Atspi.Accessible.queryComponent = lambda x: getInterface(Atspi.Accessible.get_component, x)
Atspi.Component.getAccessibleAtPoint = Atspi.Component.get_accessible_at_point
Atspi.Component.getAlpha = Atspi.Component.get_alpha
Atspi.Component.getExtents = lambda x,c: getBoundingBox(Atspi.Component.get_extents(x,c))
Atspi.Component.getLayer = Atspi.Component.get_layer
Atspi.Component.getMDIZOrder = Atspi.Component.get_mdi_z_order
Atspi.Component.getPosition = lambda x,p: pointToList(Atspi.Component.get_position(x,p))
Atspi.Component.getSize = lambda x: pointToList(Atspi.Component.get_size(x))
Atspi.Component.grabFocus = Atspi.Component.grab_focus

### document ###
Document = Atspi.Document
Atspi.Accessible.queryDocument = lambda x: getInterface(Atspi.Accessible.get_document, x)
Atspi.Document.getAttributevalue = Atspi.Document.get_attribute_value
Atspi.Document.getAttributes = lambda x: [key + ":" + value for key, value in Atspi.Document.get_attributes (x)]
Atspi.Document.getLocale = Atspi.Document.get_locale

### editable text ###
EditableText = Atspi.EditableText
Atspi.Accessible.queryEditableText = lambda x: getInterface(Atspi.Accessible.get_editable_text, x)
Atspi.EditableText.copyText = Atspi.EditableText.copy_text
Atspi.EditableText.cutText = Atspi.EditableText.cut_text
Atspi.EditableText.deleteText = Atspi.EditableText.delete_text
Atspi.EditableText.insertText = Atspi.EditableText.insert_text
Atspi.EditableText.pasteText = Atspi.EditableText.paste_text
Atspi.EditableText.setTextContents = Atspi.EditableText.set_text_contents

### hyperlink ###
Hyperlink = Atspi.Hyperlink
Atspi.Hyperlink.getObject = Atspi.Hyperlink.get_object
Atspi.Hyperlink.getURI = Atspi.Hyperlink.get_uri
Atspi.Hyperlink.isValid = Atspi.Hyperlink.is_valid
Atspi.Hyperlink.endIndex = property(fget=Atspi.Hyperlink.get_end_index)
Atspi.Hyperlink.nAnchors = property(fget=Atspi.Hyperlink.get_n_anchors)
Atspi.Hyperlink.startIndex = property(fget=Atspi.Hyperlink.get_start_index)

### hypertext ###
Hypertext = Atspi.Hypertext
Atspi.Accessible.queryHyperlink = lambda x: getInterface(Atspi.Accessible.get_hyperlink, x)
Atspi.Accessible.queryHypertext = lambda x: getInterface(Atspi.Accessible.get_hypertext, x)
Atspi.Hypertext.getLink = Atspi.Hypertext.get_link
Atspi.Hypertext.getLinkIndex = Atspi.Hypertext.get_link_index
Atspi.Hypertext.getNLinks = Atspi.Hypertext.get_n_links

### image ###
Image = Atspi.Image
Atspi.Accessible.queryImage = lambda x: getInterface(Atspi.Accessible.get_image, x)
Atspi.Image.getImageExtents = lambda x,c: getBoundingBox(Atspi.Image.get_image_extents(x,c))
Atspi.Image.getImagePosition = lambda x,p: pointToList(Atspi.Image.get_image_position(x,p))
Atspi.Image.getImageSize = lambda x: pointToList(Atspi.Image.get_image_size(x))
Atspi.Image.imageDescription = property(fget=Atspi.Image.get_image_description)
Atspi.Image.imageLocale = property(fget=Atspi.Image.get_image_locale)

### selection ###
Selection = Atspi.Selection
Atspi.Accessible.querySelection = lambda x: getInterface(Atspi.Accessible.get_selection)
Atspi.Selection.clearSelectio = Atspi.Selection.clear_selection
Atspi.Selection.deselectChild = Atspi.Selection.deselect_child
Atspi.Selection.deselectSelectedChild = Atspi.Selection.deselect_selected_child
Atspi.Selection.getSelectedChild = Atspi.Selection.get_selected_child
Atspi.Selection.isChildSelected = Atspi.Selection.is_child_selected
Atspi.Selection.selectAll = Atspi.Selection.select_all
Atspi.Selection.selectChild = Atspi.Selection.select_child
Atspi.Selection.nSelectedChildren = property(fget=Atspi.Selection.get_n_selected_children)

### table ###
Table = Atspi.Table
Atspi.Accessible.queryTable = lambda x: getInterface(Atspi.Accessible.get_table, x)
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
Atspi.Table.nColumns = property(fget=Atspi.Table.get_n_columns)
Atspi.Table.nRows = property(fget=Atspi.Table.get_n_rows)
Atspi.Table.get_nSelectedColumns = Atspi.Table.get_n_selected_columns
Atspi.Table.get_nSelectedRows = Atspi.Table.get_n_selected_rows

### text ###
Text = Atspi.Text
Atspi.Accessible.queryText = lambda x: getInterface(Atspi.Accessible.get_text, x)
Atspi.Text.addSelection = Atspi.Text.add_selection
Atspi.Text.getAttributeRun = lambda x,o,i: textAttrToList (Atspi.Text.get_attribute_run (x,o,i))
Atspi.Text.getAttributevalue = Atspi.Text.get_attribute_value
Atspi.Text.getAttributes = lambda x,o: textAttrToList (Atspi.Text.get_attributes (x, o))
Atspi.Text.getBoundedRanges = Atspi.Text.get_bounded_ranges
Atspi.Text.getcharacterAtOffset = Atspi.Text.get_character_at_offset
Atspi.Text.getCharacterExtents = lambda x,c: rectToList(Atspi.Text.get_character_extents(x,c))
Atspi.Text.getDefaultAttributeSet = lambda x: [key + ":" + value for key, value in Atspi.Text.get_default_attribute_set (x)]
Atspi.Text.getDefaultAttributes = lambda x: [key + ":" + value for key, value in Atspi.Text.get_default_attributes (x)]
Atspi.Text.getNSelections = Atspi.Text.get_n_selections
Atspi.Text.getOffsetAtPoint = Atspi.Text.get_offset_at_point
Atspi.Text.getRangeExtents = lambda x,s,e,c: rectToList(Atspi.Text.get_range_extents(x,s,e,c))
Atspi.Text.getSelection = lambda x,n: rangeToList (Atspi.Text.get_selection (x,n))
Atspi.Text.getText = Atspi.Text.get_text
Atspi.Text.getTextAfterOffset = lambda x,o,b: textRangeToList(Atspi.Text.get_text_after_offset (x,o,b))
Atspi.Text.getTextAtOffset = lambda x,o,b: textRangeToList(Atspi.Text.get_text_at_offset (x,o,b))
Atspi.Text.getTextBeforeOffset = lambda x,o,b: textRangeToList(Atspi.Text.get_text_before_offset (x,o,b))
Atspi.Text.removeSelection = Atspi.Text.remove_selection
Atspi.Text.setCaretOffset = Atspi.Text.set_caret_offset
Atspi.Text.setSelection = Atspi.Text.set_selection
Atspi.Text.caretOffset = property(fget=Atspi.Text.get_caret_offset, fset=Atspi.Text.set_caret_offset)
Atspi.Text.characterCount = property(fget=Atspi.Text.get_character_count)

TEXT_BOUNDARY_CHAR = Atspi.TextBoundaryType.CHAR
TEXT_BOUNDARY_WORD_START = Atspi.TextBoundaryType.WORD_START
TEXT_BOUNDARY_WORD_END = Atspi.TextBoundaryType.WORD_END
TEXT_BOUNDARY_SENTENCE_START = Atspi.TextBoundaryType.SENTENCE_START
TEXT_BOUNDARY_SENTENCE_END = Atspi.TextBoundaryType.SENTENCE_END
TEXT_BOUNDARY_LINE_START = Atspi.TextBoundaryType.LINE_START
TEXT_BOUNDARY_LINE_END = Atspi.TextBoundaryType.LINE_END

TEXT_CLIP_NONE = Atspi.TextClipType.NONE
TEXT_CLIP_MIN = Atspi.TextClipType.MIN
TEXT_CLIP_MAX= Atspi.TextClipType.MAX
TEXT_CLIP_BOTH= Atspi.TextClipType.BOTH

### value ###
Value = Atspi.Value
Atspi.Accessible.queryValue = lambda x: getInterface(Atspi.Accessible.get_value, x)
Atspi.Value.currentValue = property(fget=Atspi.Value.get_current_value, fset=Atspi.Value.set_current_value)
Atspi.Value.maximumValue = property(fget=Atspi.Value.get_maximum_value)
Atspi.Value.minimumIncrement = property(fget=Atspi.Value.get_minimum_increment)
Atspi.Value.minimumValue = property(fget=Atspi.Value.get_minimum_value)

### event ###
Atspi.Event.host_application = property(fget=lambda x: x.source.get_application())

### RelationSet ###
Atspi.Relation.getRelationType = Atspi.Relation.get_relation_type
Atspi.Relation.getNTargets = Atspi.Relation.get_n_targets
Atspi.Relation.getTarget = Atspi.Relation.get_target
RELATION_NULL = Atspi.RelationType.NULL
RELATION_LABEL_FOR = Atspi.RelationType.LABEL_FOR
RELATION_LABELLED_BY = Atspi.RelationType.LABELLED_BY
RELATION_CONTROLLER_FOR = Atspi.RelationType.CONTROLLER_FOR
RELATION_CONTROLLED_BY = Atspi.RelationType.CONTROLLED_BY
RELATION_MEMBER_OF = Atspi.RelationType.MEMBER_OF
RELATION_TOOLTIP_FOR = Atspi.RelationType.TOOLTIP_FOR
RELATION_NODE_CHILD_OF = Atspi.RelationType.NODE_CHILD_OF
RELATION_NODE_PARENT_OF = Atspi.RelationType.NODE_PARENT_OF
RELATION_EXTENDED = Atspi.RelationType.EXTENDED
RELATION_FLOWS_TO = Atspi.RelationType.FLOWS_TO
RELATION_FLOWS_FROM = Atspi.RelationType.FLOWS_FROM
RELATION_SUBWINDOW_OF = Atspi.RelationType.SUBWINDOW_OF
RELATION_EMBEDS = Atspi.RelationType.EMBEDS
RELATION_POPUP_FOR = Atspi.RelationType.POPUP_FOR
RELATION_PARENT_WINDOW_OF = Atspi.RelationType.PARENT_WINDOW_OF
RELATION_DESCRIPTION_FOR = Atspi.RelationType.DESCRIPTION_FOR
RELATION_DESCRIBED_BY = Atspi.RelationType.DESCRIBED_BY

# Build a dictionary mapping relation values to names based on the prefix of the enum constants.

RELATION_VALUE_TO_NAME = dict(((value, name[9:].lower().replace('_', ' ')) 
                               for name, value 
                               in globals().items()
                               if name.startswith('RELATION_')))

### ModifierType ###
MODIFIER_SHIFT = Atspi.ModifierType.SHIFT
MODIFIER_SHIFTLOCK = Atspi.ModifierType.SHIFTLOCK
MODIFIER_CONTROL = Atspi.ModifierType.CONTROL
MODIFIER_ALT = Atspi.ModifierType.ALT
MODIFIER_META = Atspi.ModifierType.META
MODIFIER_META2 = Atspi.ModifierType.META2
MODIFIER_META3 = Atspi.ModifierType.META3
MODIFIER_NUMLOCK = Atspi.ModifierType.NUMLOCK

### EventType ###
KEY_PRESSED_EVENT = Atspi.EventType.KEY_PRESSED_EVENT
KEY_RELEASED_EVENT = Atspi.EventType.KEY_RELEASED_EVENT
BUTTON_PRESSED_EVENT = Atspi.EventType.BUTTON_PRESSED_EVENT
BUTTON_RELEASED_EVENT = Atspi.EventType.BUTTON_RELEASED_EVENT
