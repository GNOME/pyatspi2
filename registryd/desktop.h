/*
 * AT-SPI - Assistive Technology Service Provider Interface
 * (Gnome Accessibility Project; http://developer.gnome.org/projects/gap)
 *
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

#ifndef SPI_DESKTOP_H_
#define SPI_DESKTOP_H_

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include <bonobo/bonobo-xobject.h>
#include <atk/atkobject.h>
#include <accessible.h>
#include <application.h>
#include <libspi/Accessibility.h>

#define SPI_DESKTOP_TYPE        (spi_desktop_get_type ())
#define SPI_DESKTOP(o)          (G_TYPE_CHECK_INSTANCE_CAST ((o), SPI_DESKTOP_TYPE, SpiDesktop))
#define SPI_DESKTOP_CLASS(k)    (G_TYPE_CHECK_CLASS_CAST((k), SPI_DESKTOP_TYPE, SpiDesktopClass))
#define IS_SPI_DESKTOP(o)       (G_TYPE_CHECK__INSTANCE_TYPE ((o), SPI_DESKTOP_TYPE))
#define IS_SPI_DESKTOP_CLASS(k) (G_TYPE_CHECK_CLASS_TYPE ((k), SPI_DESKTOP_TYPE))

typedef struct {
        SpiAccessible parent;
        GList *applications; /* TODO: maybe change this so it's generated on-demand ? */
} SpiDesktop;

typedef struct {
        SpiAccessibleClass parent_class;
        POA_Accessibility_SpiDesktop__epv epv;
} SpiDesktopClass;

GType               spi_desktop_get_type           (void);
void                spi_desktop_add_application    (SpiApplication *app);
void                spi_desktop_remove_application (SpiApplication *app);
SpiDesktop             *spi_desktop_new               (void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SPI_DESKTOP_H_ */
