/*
 * Copyright 2008 Codethink Ltd.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */

#ifndef MY_ATK_TEXT_H
#define MY_ATK_TEXT_H
/*
 * MyAtkText: implements AtkText and AtkEditableText
 */
#include <atk/atk.h>

#include "my-atk-object.h"
	
#define MY_TYPE_ATK_TEXT             (my_atk_text_get_type ())
#define MY_ATK_TEXT(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), MY_TYPE_ATK_TEXT, MyAtkText))
#define MY_ATK_TEXT_CLASS(vtable)    (G_TYPE_CHECK_CLASS_CAST ((vtable), MY_TYPE_ATK_TEXT, MyAtkTextClass))
#define MY_IS_ATK_TEXT(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), MY_TYPE_ATK_TEXT))
#define MY_IS_ATK_TEXT_CLASS(vtable) (G_TYPE_CHECK_CLASS_TYPE ((vtable), MY_TYPE_ATK_TEXT))
#define MY_ATK_TEXT_GET_CLASS(inst)  (G_TYPE_INSTANCE_GET_CLASS ((inst), MY_TYPE_ATK_TEXT, MyAtkTextClass))

typedef struct _MyAtkText MyAtkText;
typedef struct _MyAtkTextClass MyAtkTextClass;

//Struct, describing bounds of one selection.
typedef struct
{
    gint start_offset, end_offset;
}TextSelection;
//Struct, describing values, needed for determine extent of characters 
typedef struct
{
    gint base_x, base_y;//coordinates of the top-left corner of text
    gint pixels_above_line;
    gint pixels_below_line;
    gint size;//size of the character(height in pixels)
    gint pixels_between_characters;//monoscaped font
    gint width;//width of character
}TextBounds; 

struct _MyAtkText
{
    MyAtkObject parent;
    
    gchar* str;//string, containing text
    GList* attributes;//running atributes
    AtkAttributeSet *default_attributes;//default attributes
    
    TextBounds bounds;
    
    GArray* selections;
    
    gint caret_offset;
};

struct _MyAtkTextClass
{
    MyAtkObjectClass parent;
    gchar* clipboard;
};

GType my_atk_text_get_type();

void my_atk_text_interface_init(gpointer g_iface, gpointer iface_data);
#endif /*MY_ATK_TEXT_H*/
