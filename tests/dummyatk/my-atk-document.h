/*
 * Copyright 2010 Mike Gorse <mgorse@novell.com>
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
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#ifndef MY_ATK_DOCUMENT_H
#define MY_ATK_DOCUMENT_H

#include <glib-object.h>
#include <atk/atk.h> 
#include <my-atk-object.h>
    
#define MY_TYPE_ATK_DOCUMENT             (my_atk_document_get_type ())
#define MY_ATK_DOCUMENT(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), MY_TYPE_ATK_DOCUMENT, MyAtkDocument))
#define MY_ATK_DOCUMENT_CLASS(vdocument)    (G_TYPE_CHECK_CLASS_CAST ((vdocument), MY_TYPE_ATK_DOCUMENT, MyAtkDocumentClass))
#define MY_IS_ATK_DOCUMENT(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), MY_TYPE_ATK_DOCUMENT))
#define MY_IS_ATK_DOCUMENT_CLASS(vdocument) (G_TYPE_CHECK_CLASS_TYPE ((vdocument), MY_TYPE_ATK_DOCUMENT))
#define MY_ATK_DOCUMENT_GET_CLASS(inst)  (G_TYPE_INSTANCE_GET_CLASS ((inst), MY_TYPE_ATK_DOCUMENT, MyAtkDocumentClass))

// default string values
#define DEF_LOCALE_TEXT  "en-US"
#define DEF_TYPE_TEXT    "default type"

typedef struct _MyAtkDocument MyAtkDocument;
typedef struct _MyAtkDocumentClass MyAtkDocumentClass;

struct _MyAtkDocument 
{
    MyAtkObject parent;
        
    gboolean disposed;
    
  gchar *locale;
  gchar *document_type;
};

struct _MyAtkDocumentClass 
{
    MyAtkObjectClass parent;
};

GType 
my_atk_document_get_type (void);

#endif /*MY_ATK_DOCUMENT_H*/
