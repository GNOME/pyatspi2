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

#ifndef USEFUL_FUNCTIONS_H
#define USEFUL_FUNCTIONS_H
/*
 * Functions and macros widely used in the tests.
 */
 
//macro for creating objects in startup section
#define OBJECT_NEW(obj, type, type_str) obj = g_object_new(type,NULL);\
    if(obj == NULL)\
    {\
        INIT_FAILED("Cannot create instance of type" type_str ".\n");\
    }
//macro for destroying object 
#define OBJECT_UNREF(obj) if(obj != NULL)\
    {\
        g_object_unref((gpointer)obj);\
    }
//for testing signals
#define HANDLER_DISCONNECT(obj, h) if((h) != 0)\
	{\
		g_signal_handler_disconnect(obj, h);\
	}

gboolean my_strcmp(const gchar* str1, const gchar* str2);

gint my_strlen(const gchar* str);

gboolean my_strncmp(const gchar* str1, const gchar* str2, gint n);

#endif /*USEFUL_FUNCTIONS_H*/
