AC_INIT([pyatspi], [2.38.1], [accessibility-atspi@lists.linux-foundation.org])
AC_CONFIG_AUX_DIR(config)

# The version of python used is determined by the executable pointed to by the
# --with-python switch, or if that's not set, by the PYTHON environment
# variable.  For instance if your system installs Python 3 as python3 to
# configure to compile pygobject under Python 3 you would do this:
#   $ ./configure --with-python=python3
# or
#   $ PYTHON=python3 ./configure
#
# You can also build against a full interpreter path, such as
#   $ ./configure --with-python=~/my-patched-python/python

LT_RELEASE=$AT_SPI_MAJOR_VERSION.$AT_SPI_MINOR_VERSION
LT_CURRENT=0
LT_REVISION=0
LT_AGE=0
LT_VERSION_INFO='-version-info ${LT_CURRENT}:${LT_REVISION}:${LT_AGE}'
AC_SUBST(LT_VERSION_INFO)
AC_SUBST(LT_RELEASE)
AC_SUBST(LT_CURRENT)
AC_SUBST(LT_REVISION)
AC_SUBST(LT_AGE)

AM_INIT_AUTOMAKE([-Wall foreign no-dist-gzip dist-xz])

AC_PROG_CC

# option to specify python interpreter to use; this just sets $PYTHON, so that
# we will fallback to reading $PYTHON if --with-python is not given, and
# python.m4 will get the expected input
AC_ARG_WITH(python,
  AC_HELP_STRING([--with-python=PATH], [Path to Python interpreter; searches $PATH if only a program name is given; if not given, searches for a few standard names such as "python3" or "python2"]),
  [PYTHON="$withval"], [])
if test x"$PYTHON" = xyes; then
	AC_MSG_ERROR([--with-python option requires a path or program argument])
fi
if test -n "$PYTHON" && ! which "$PYTHON"; then
	AC_MSG_ERROR([Python interpreter $PYTHON does not exist])
fi

AM_PATH_PYTHON(2.6)
AM_DISABLE_STATIC
AM_PROG_LIBTOOL
PKG_PROG_PKG_CONFIG

AC_CONFIG_HEADERS([config.h])

AC_MSG_CHECKING([whether tests are enabled])
AC_ARG_ENABLE(tests,
              [AS_HELP_STRING([--enable-tests], [Build with testing enabled])],
              enable_tests=$enableval,
              enable_tests=no)
AC_MSG_RESULT($enable_tests)
AM_CONDITIONAL(ENABLE_TESTING, test x$enable_tests = xyes)

if test "$enable_tests" = "yes"; then
        AM_CHECK_PYMOD(dbus, , , [AC_MSG_ERROR(Could not find python module: dbus)])

        PKG_CHECK_MODULES(DBUS, [dbus-1 >= 1.0])
        AC_SUBST(DBUS_LIBS)
        AC_SUBST(DBUS_CFLAGS)

        PKG_CHECK_MODULES(GLIB, [glib-2.0])
        AC_SUBST(GLIB_LIBS)
        AC_SUBST(GLIB_CFLAGS)

        PKG_CHECK_MODULES(AT_SPI, [atspi-2])
        AC_SUBST(AT_SPI_LIBS)
        AC_SUBST(AT_SPI_CFLAGS)

        PKG_CHECK_MODULES(GOBJ, [gobject-2.0 >= 2.0.0])
        AC_SUBST(GOBJ_LIBS)
        AC_SUBST(GOBJ_CFLAGS)

        PKG_CHECK_MODULES(GMODULE, [gmodule-2.0 >= 2.0.0])	
        AC_SUBST(GMODULE_LIBS)
        AC_SUBST(GMODULE_CFLAGS)

        PKG_CHECK_MODULES(LIB_XML, [libxml-2.0 >= 2.0.0])
        AC_SUBST(LIB_XML_LIBS)
        AC_SUBST(LIB_XML_CFLAGS)

        PKG_CHECK_MODULES(ATK, [atk >= 2.11.2])
        AC_SUBST(ATK_LIBS)
        AC_SUBST(ATK_CFLAGS)

        PKG_CHECK_MODULES(GTK, [gtk+-3.0])
        AC_SUBST(GTK_LIBS)
        AC_SUBST(GTK_CFLAGS)
fi

        PKG_CHECK_MODULES(PYGOBJ, [pygobject-3.0 >= 2.90.1])

AM_CONDITIONAL(SET_GTK_MODULE, test -z "$GTK_MODULE_DIR")
AC_ARG_VAR([GTK_MODULE_DIR], [Where to find the atk-adaptor gtk module])
if test -z "$GTK_MODULE_DIR"; then
	  GTK_MODULE_DIR=gtk-2.0/modules
fi

AC_PATH_XTRA

AC_CONFIG_FILES([Makefile
		 tests/Makefile
		 tests/dummyatk/Makefile
		 tests/data/Makefile
		 tests/pyatspi/Makefile
		 tests/pyatspi/testrunner
		 tests/pyatspi/pasytest/Makefile
		 tests/apps/Makefile
		 pyatspi/Makefile
		 examples/Makefile
		])

AC_OUTPUT
