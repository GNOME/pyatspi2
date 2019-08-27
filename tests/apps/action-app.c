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

static AtkObject *root_accessible;

G_MODULE_EXPORT void
test_init (gchar *path)
{
  root_accessible  = g_object_new(MY_TYPE_ATK_ACTION, NULL);
  root_accessible->name = g_strdup ("atspi-test-main");
  root_accessible->role = ATK_ROLE_APPLICATION;
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
  return root_accessible;
}
