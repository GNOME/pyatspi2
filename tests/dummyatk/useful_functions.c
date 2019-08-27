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

#include <string.h>
#include <glib.h>
/*
 * Functions and macros widely used in the tests.
 */
 
//same as strcmp() == 0 but works properly for NULL pointers
gboolean my_strcmp(const gchar* str1, const gchar* str2)
{
    if(str1 == str2) return TRUE;
    if(str1 == NULL || str2 == NULL) return FALSE;
    
    return strcmp(str1,str2) == 0;
}
//same as strlen but works properly for NULL pointer and returns gint instead of guint
gint my_strlen(const gchar* str)
{
    if(str == NULL)return 0;
    return (gint)strlen(str);
}
//same as strncmp() == 0 but works properly for NULL pointers
gboolean my_strncmp(const gchar* str1, const gchar* str2, gint n)
{
    if(n <= 0)return TRUE;
    if(str1 == str2)return TRUE;
    if(str1 == NULL || str2 == NULL)return FALSE;

    return strncmp(str1, str2, n) == 0;
}
