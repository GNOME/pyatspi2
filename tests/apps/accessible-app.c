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

#include "atk-object-xml-loader.h"

static gchar *tdata_path = NULL;

static AtkObject *root_accessible;

static AtkStateType states[] =
{
  ATK_STATE_MULTI_LINE,
  ATK_STATE_MODAL,
  ATK_STATE_INDETERMINATE,
  ATK_STATE_SUPPORTS_AUTOCOMPLETION,
  ATK_STATE_VERTICAL
};

#define OBJECT_TEST_1 "accessible-test.xml"

G_MODULE_EXPORT void
test_init (gchar *path)
{
  AtkStateSet *ss;
  gchar *td;

  if (path == NULL)
     g_error("No test data path provided");
  tdata_path = path;

  td = g_build_path(G_DIR_SEPARATOR_S, tdata_path, OBJECT_TEST_1, NULL);
  root_accessible = ATK_OBJECT(atk_object_xml_parse(td));
  g_free(td);

  ss = atk_object_ref_state_set(ATK_OBJECT(root_accessible));
  atk_state_set_add_states(ss, states, 5);
  g_object_unref(G_OBJECT(ss));
}

G_MODULE_EXPORT void
test_next (int argc, char *argv[])
{
  ;
}

G_MODULE_EXPORT void
test_finished (int argc, char *argv[])
{
  ;
}

G_MODULE_EXPORT AtkObject *
test_get_root (void)
{
  return root_accessible;
}
