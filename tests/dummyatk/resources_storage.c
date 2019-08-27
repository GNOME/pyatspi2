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

#include <atk/atk.h>

GHashTable* resources = NULL;

void resource_storage_init()
{
    if(resources == NULL)
    resources = g_hash_table_new_full(g_str_hash, g_str_equal,
        (GDestroyNotify)g_free, (GDestroyNotify)g_object_unref);
}

void resource_storage_free()
{
    if(resources == NULL) return;
    g_hash_table_destroy(resources);
    resources = NULL;
}

void resource_storage_add(const gchar* name, AtkObject* resource)
{
    if(resources == NULL) return;
    g_hash_table_insert(resources, g_strdup(name), g_object_ref(resource));
}

AtkObject* resource_storage_get(const gchar* name)
{
    if(resources == NULL) return NULL;
    return g_hash_table_lookup(resources, name);
}
void resources_storage_remove(const gchar* name)
{
    if(resources == NULL) return;
    g_hash_table_remove(resources, name);
}
