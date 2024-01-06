Pyatspi  
------------

AT-SPI is a library and set of DBus protocols that allow access technology
such as a screen reader to programmatically inspect the information that
applications are presenting. It can also be used in automated testing. Pyatspi
is a Python wrapper around libatspi, which, in turn, provides a convenient
AT-side wrapper around the DBus protocols. Pyatspi exists primarily for
historical reasons; libatspi is GObject-based and can be used in python
directly through GObject introspection. For new applications, it is
recommended to use the libatspi gobject-introspection binding directly,
rather than using pyatspi. Going forward, pyatspi is unlikely to be
actively maintained aside from fixing bugs.

For bug reports, patches or enhancements please use:

        https://gitlab.gnome.org/GNOME/pyatspi2/issues/

A git repository with the latest development code is available at:

        https://gitlab.gnome.org/GNOME/pyatspi2

Code in this repository depends on at-spi2-core resources. The
at-spi2-core repository can be found at:

        https://gitlab.gnome.org/GNOME/at-spi2-core

Other sources of relevant information about AT-SPI and Accessibility
include:

        https://wiki.gnome.org/Accessibility



Contents of this package  
------------------------

This package includes a python client library for the AT-SPI D-Bus accessibility infrastructure.
