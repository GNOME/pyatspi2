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

#ifndef MY_ATK_STREAMABLE_CONTENT_H
#define MY_ATK_STREAMABLE_CONTENT_H

/*
 * MyAtkStreamableContent: derives GObject and implements AtkStreamableContent
 */

#include <atk/atk.h>

#include "my-atk-object.h"

#define MY_TYPE_ATK_STREAMABLE_CONTENT             (my_atk_streamable_content_get_type ())
#define MY_ATK_STREAMABLE_CONTENT(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), MY_TYPE_ATK_STREAMABLE_CONTENT, MyAtkStreamableContent))
#define MY_ATK_STREAMABLE_CONTENT_CLASS(vtable)    (G_TYPE_CHECK_CLASS_CAST ((vtable), MY_TYPE_ATK_STREAMABLE_CONTENT, MyAtkStreamableContentClass))
#define MY_IS_ATK_STREAMABLE_CONTENT(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), MY_TYPE_ATK_STREAMABLE_CONTENT))
#define MY_IS_ATK_STREAMABLE_CONTENT_CLASS(vtable) (G_TYPE_CHECK_CLASS_TYPE ((vtable), MY_TYPE_ATK_STREAMABLE_CONTENT))
#define MY_ATK_STREAMABLE_CONTENT_GET_CLASS(inst)  (G_TYPE_INSTANCE_GET_CLASS ((inst), MY_TYPE_ATK_STREAMABLE_CONTENT, MyAtkStreamableContentClass))

typedef struct _MyAtkStreamableContent MyAtkStreamableContent;
typedef struct _MyAtkStreamableContentClass MyAtkStreamableContentClass;

static const gchar* mime_types[]={"text/plain", "text/richtext"};
static const gchar* file_names[]={"file1", "file2"};
struct _MyAtkStreamableContent
{
    MyAtkObject parent;
};

struct _MyAtkStreamableContentClass
{
    MyAtkObjectClass parent;
};

GType my_atk_streamable_content_get_type();
#endif /*MY_ATK_STREAMABLE_CONTENT_H*/
