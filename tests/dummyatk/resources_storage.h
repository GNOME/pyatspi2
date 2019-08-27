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

#ifndef RESOURCES_STORAGE_H
#define RESOURCES_STORAGE_H

#include <glib.h>

void resource_storage_init();

void resource_storage_free();

void resource_storage_add(const gchar* name, AtkObject* resource);

AtkObject* resource_storage_get(const gchar* name);

void resources_storage_remove(const gchar* name);

#endif /*RESOURCES_STORAGE_H*/
