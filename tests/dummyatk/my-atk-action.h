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

#ifndef MY_ATK_ACTION_H
#define MY_ATK_ACTION_H
//Object, which implement interface AtkAction(all functions)
#include <glib.h>
#include <glib-object.h>
#include <atk/atk.h>

#include "my-atk-object.h"

//declarations
#define MY_TYPE_ATK_ACTION             (my_atk_action_get_type ())
#define MY_ATK_ACTION(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), MY_TYPE_ATK_ACTION, MyAtkAction))
#define MY_ATK_ACTION_CLASS(vtable)    (G_TYPE_CHECK_CLASS_CAST ((vtable), MY_TYPE_ATK_ACTION, MyAtkActionClass))
#define MY_IS_ATK_ACTION(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), MY_TYPE_ATK_ACTION))
#define MY_IS_ATK_ACTION_CLASS(vtable) (G_TYPE_CHECK_CLASS_TYPE ((vtable), MY_TYPE_ATK_ACTION))
#define MY_ATK_ACTION_GET_CLASS(inst)  (G_TYPE_INSTANCE_GET_CLASS ((inst), MY_TYPE_ATK_ACTION, MyAtkActionClass))


#define FIRST_ACTION_NAME "First action"
#define FIRST_ACTION_DESCRIPTION "First action performed"
#define FIRST_ACTION_KEYBINDING "0"

#define DEFAULT_NUMBER_ACTIONS 10
#define DEFAULT_ACTION_NAME "Action"
#define DEFAULT_ACTION_DESCRIPTION "Description of action"
#define DEFAULT_ACTION_KEYBINDING keybinding_note_define


//for external using
#define LAST_PERFORMED_ACTION(myAtkAction) (MY_ATK_ACTION(myAtkAction)->last_performed_action)
#define CLEAR_LAST_PERFOMED_ACTION(myAtkAction) (MY_ATK_ACTION(myAtkAction)->last_performed_action = -1

typedef struct _MyAtkAction MyAtkAction;
typedef struct _MyAtkActionClass MyAtkActionClass;

struct _MyAtkAction
{
    MyAtkObject parent;

    gboolean disposed;
    struct OneAction
    {
        gchar *name;
        gchar *description;
        gchar *keybinding;
    }*actions;
    gint n;
    gint last_performed_action;//this field is changed when perfoms action
};

struct _MyAtkActionClass
{
    MyAtkObjectClass parent;
};
GType my_atk_action_get_type(void);

#endif /*MY_ATK_ACTION_H*/
