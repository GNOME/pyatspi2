/*
 * Copyright 2010 Novell, Inc.
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

/* This file contains both declaration and definition of the MyAtkDocument,
 * a GObject that pretends to implement the AtkDocumentIface interface (it 
 * registers appropriate interface), but provides no implementation for any of the
 * methods of this interface (NULL-filled vftbl).
 */

#include <glib-object.h>
#include <atk/atk.h> 

#include "my-atk-object.h"
#include "my-atk-document.h"
    
///////////////////////////////////////////////////////////////////////////
// Helper functions and data
///////////////////////////////////////////////////////////////////////////
const gchar *
my_atk_document_get_document_locale (AtkDocument *document)
{
  return DEF_LOCALE_TEXT;
}

const gchar *
my_atk_document_get_document_type (AtkDocument *document)
{
  return DEF_TYPE_TEXT;
}

AtkAttributeSet *
my_atk_document_get_document_attributes (AtkDocument *document)
{
  /* TODO: Implement */
  return NULL;
}

const gchar *
my_atk_document_get_document_attribute_value (AtkDocument *document, const gchar *value)
{
  /*( TODO: Implement */
  return NULL;
}

///////////////////////////////////////////////////////////////////////////
// Implementation
///////////////////////////////////////////////////////////////////////////
static GObjectClass *parent_class_document = NULL;

/******************************************************************/
static void
document_interface_init (gpointer g_iface, gpointer iface_data)
{
    AtkDocumentIface *klass = (AtkDocumentIface *)g_iface;
    
    /* set up overrides here */
    klass-> get_document_type = my_atk_document_get_document_type;
    klass-> get_document_locale = my_atk_document_get_document_locale;
    klass-> get_document_attributes = my_atk_document_get_document_attributes;
    klass-> get_document_attribute_value = my_atk_document_get_document_attribute_value;
}

static void
document_instance_init (GTypeInstance *instance, gpointer g_class)
{
    MyAtkDocument *self = (MyAtkDocument *)instance;
    
    self->disposed = FALSE;
}

static void
my_atk_document_dispose (GObject *obj)
{
    MyAtkDocument *self = (MyAtkDocument *)obj;

    if (self->disposed) 
    {
        return;
    }
    
    /* Make sure dispose does not run twice. */
    self->disposed = TRUE;

    /* Chain up to the parent class */
    G_OBJECT_CLASS (parent_class_document)->dispose (obj);
}

static void
my_atk_document_finalize (GObject *obj)
{
    /* Chain up to the parent class */
    G_OBJECT_CLASS (parent_class_document)->finalize (obj);
}

static void
my_atk_document_class_init (gpointer g_class, gpointer g_class_data)
{
    GObjectClass *gobject_class = G_OBJECT_CLASS (g_class);
    MyAtkDocumentClass *klass = MY_ATK_DOCUMENT_CLASS (g_class);

    gobject_class->dispose = my_atk_document_dispose;
    gobject_class->finalize = my_atk_document_finalize;

    parent_class_document = g_type_class_peek_parent (klass);
}

GType 
my_atk_document_get_type (void)
{
    static GType type = 0;
    if (type == 0) 
    {
        static const GTypeInfo info = 
        {
            sizeof (MyAtkDocumentClass),
            NULL,   /* base_init */
            NULL,   /* base_finalize */
            my_atk_document_class_init, /* class_init */
            NULL,   /* class_finalize */
            NULL,   /* class_data */
            sizeof (MyAtkDocument),
            0,      /* n_preallocs */
            document_instance_init    /* instance_init */
        };
                
        static const GInterfaceInfo iface_info = 
        {
            (GInterfaceInitFunc) document_interface_init,    /* interface_init */
            NULL,                                       /* interface_finalize */
            NULL                                        /* interface_data */
        };
        type = g_type_register_static (MY_TYPE_ATK_OBJECT,
                                       "MyAtkDocumentType",
                                       &info, 0);
        g_type_add_interface_static (type,
                                     ATK_TYPE_DOCUMENT,
                                     &iface_info);
    }
    return type;
}
