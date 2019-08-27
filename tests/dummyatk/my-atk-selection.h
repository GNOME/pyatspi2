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

/* This file contains both declaration and definition of the MyAtkSelection,
 * a GObject that implements the AtkSelectionIface interface.
 */

#ifndef MY_ATK_SELECTION_H
#define MY_ATK_SELECTION_H

#include <glib-object.h>
#include <atk/atk.h> 

#include <my-atk-object.h>

#define MY_TYPE_ATK_SELECTION             (my_atk_selection_get_type ())
#define MY_ATK_SELECTION(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), MY_TYPE_ATK_SELECTION, MyAtkSelection))
#define MY_ATK_SELECTION_CLASS(vtable)    (G_TYPE_CHECK_CLASS_CAST ((vtable), MY_TYPE_ATK_SELECTION, MyAtkSelectionClass))
#define MY_IS_ATK_SELECTION(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), MY_TYPE_ATK_SELECTION))
#define MY_IS_ATK_SELECTION_CLASS(vtable) (G_TYPE_CHECK_CLASS_TYPE ((vtable), MY_TYPE_ATK_SELECTION))
#define MY_ATK_SELECTION_GET_CLASS(inst)  (G_TYPE_INSTANCE_GET_CLASS ((inst), MY_TYPE_ATK_SELECTION, MyAtkSelectionClass))

/* Number of child objects for the MyAtkSelection instance */
#define TEST_SELECTION_NCHILDREN 10    

typedef struct _MyAtkSelection MyAtkSelection;
typedef struct _MyAtkSelectionClass MyAtkSelectionClass;

struct _MyAtkSelection 
{
    MyAtkObject parent;
        
    gboolean disposed;
    
    /* TRUE if multiple selection is supported, FALSE otherwise.
     * default - TRUE.
     */
    gboolean multisel_supported;
    
    /* Children of this object */
    MyAtkObject* child[TEST_SELECTION_NCHILDREN];
    
    /* is_selected[i] == TRUE means the ith child is selected, == FALSE - 
     * it is not.
     */
    gboolean is_selected[TEST_SELECTION_NCHILDREN];
};

struct _MyAtkSelectionClass 
{
    MyAtkObjectClass parent;
};

GType 
my_atk_selection_get_type (void);

#endif /*MY_ATK_SELECTION_H*/

