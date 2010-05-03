if SET_GTK_MODULE
if RELOCATE
gtk_module_dir = $(libdir)/$(GTK_MODULE_DIR)/at-spi-dbus/modules
else
gtk_module_dir = $(libdir)/$(GTK_MODULE_DIR)
endif
else
gtk_module_dir = $(GTK_MODULE_DIR)
endif

SUBDIRS = pasytest

EXTRA_DIST = \
	accessibletest.py\
	actiontest.py\
	componenttest.py\
	desktoptest.py\
	statetest.py\
	Makefile.am\
	Makefile.in\
	setvars.sh\
	relationtest.py\
	runtests.sh\
	testrunner

TESTS_ENVIRONMENT = top_builddir=$(top_builddir) top_srcdir=$(top_srcdir) gtk_module_dir=$(gtk_module_dir)

TESTS = runtests.sh

CLEANFILES = *.pyc
