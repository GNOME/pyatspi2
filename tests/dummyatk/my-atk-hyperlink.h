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

#ifndef MY_ATK_HYPERLINK_H
#define MY_ATK_HYPERLINK_H
/*
 * MyAtkHyperlink: implements AtkHyperlink
 */
#include <atk/atk.h>

#define MY_TYPE_ATK_HYPERLINK             (my_atk_hyperlink_get_type ())
#define MY_ATK_HYPERLINK(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), MY_TYPE_ATK_HYPERLINK, MyAtkHyperlink))
#define MY_ATK_HYPERLINK_CLASS(vtable)    (G_TYPE_CHECK_CLASS_CAST ((vtable), MY_TYPE_ATK_HYPERLINK, MyAtkHyperlinkClass))
#define MY_IS_ATK_HYPERLINK(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), MY_TYPE_ATK_HYPERLINK))
#define MY_IS_ATK_HYPERLINK_CLASS(vtable) (G_TYPE_CHECK_CLASS_TYPE ((vtable), MY_TYPE_ATK_HYPERLINK))
#define MY_ATK_HYPERLINK_GET_CLASS(inst)  (G_TYPE_INSTANCE_GET_CLASS ((inst), MY_TYPE_ATK_HYPERLINK, MyAtkHyperlinkClass))

typedef struct _MyAtkHyperlink MyAtkHyperlink;
typedef struct _MyAtkHyperlinkClass MyAtkHyperlinkClass;

struct _MyAtkHyperlink
{
    AtkHyperlink parent;
    
    gint start_index, end_index;
    
    gchar* uri;
    gint number_of_anchors;//0 on "clear" hyperlink and 1 after set it
    gboolean is_selected;
};

struct _MyAtkHyperlinkClass
{
    AtkHyperlinkClass parent;
};

MyAtkHyperlink* my_atk_hyperlink_new(gint start_index, gint end_index,const gchar* uri);

GType my_atk_hyperlink_get_type();
#endif /*MY_ATK_HYPERLINK_H*/
