/* ATK -  Accessibility Toolkit
 * Copyright 2001 Sun Microsystems Inc.
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
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#ifndef TEXT_H_
#define TEXT_H_


#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include <bonobo/bonobo-object.h>
#include <atk/atk.h>
#include <libspi/Accessibility.h>

#define TEXT_TYPE        (text_get_type ())
#define TEXT(obj)          (G_TYPE_CHECK_INSTANCE_CAST ((obj), TEXT_TYPE, Text))
#define TEXT_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), TEXT_TYPE, TextClass))
#define IS_TEXT(obj)       (G_TYPE_CHECK__INSTANCE_TYPE ((obj), TEXT_TYPE))
#define IS_TEX_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), TEXT_TYPE))

typedef struct _Text Text;
typedef struct _TextClass TextClass;

struct _Text {
  BonoboObject parent;
  AtkObject *atko;
};

struct _TextClass {
  BonoboObjectClass parent_class;
  POA_Accessibility_Text__epv epv;
};

GType
text_get_type   (void);

Text *
text_interface_new       (AtkObject *obj);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TEXT_H_ */
