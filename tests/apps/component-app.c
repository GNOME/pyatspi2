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

#include <gmodule.h>
#include <atk/atk.h>
#include <my-atk.h>

static gchar *tdata_path = NULL;

static AtkComponent *comps[] = {NULL, NULL, NULL};
static const AtkRectangle extents[] = {{0,0,30,20}, {40,30,30,40}, {0,0,70,70}};
static const AtkLayer layers[] = {ATK_LAYER_WINDOW, ATK_LAYER_WIDGET, ATK_LAYER_MDI};
static const guint zorders[] = {0, -100, 100};
static const gboolean extent_may_changed[] = {TRUE, FALSE, TRUE};

G_MODULE_EXPORT void
test_init (gchar *path)
{
  int i;
  AtkObject *atk;

  if (path == NULL)
     g_error("No test data path provided");
  tdata_path = path;

  for(i = 0; i < sizeof(comps) / sizeof(comps[0]); i++)
    {
      MyAtkComponent *mycomp = MY_ATK_COMPONENT(g_object_new(MY_TYPE_ATK_COMPONENT, NULL));
        
      mycomp->extent = extents[i];
      mycomp->is_extent_may_changed = extent_may_changed[i];
      mycomp->layer = layers[i];
      mycomp->zorder = zorders[i];
      
      comps[i] = ATK_COMPONENT(mycomp);
    }
    
  my_atk_object_add_child(MY_ATK_OBJECT(comps[2]), MY_ATK_OBJECT(comps[0]));
  my_atk_object_add_child(MY_ATK_OBJECT(comps[2]), MY_ATK_OBJECT(comps[1]));

    atk = ATK_OBJECT (comps [2]);
    atk->name = g_strdup ("atspi-test-main");
    atk->role = ATK_ROLE_APPLICATION;
}

G_MODULE_EXPORT void
test_next (int argc, char *argv[])
{
  g_print("Moving to next stage\n");
}

G_MODULE_EXPORT void
test_finished (int argc, char *argv[])
{
  g_print("Test has completed\n");
}

G_MODULE_EXPORT AtkObject *
test_get_root (void)
{
  return ATK_OBJECT(comps[2]);
}
