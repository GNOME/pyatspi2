SUBDIRS=busutils
if RELOCATE
pyatspidir = $(pythondir)/pyatspi_dbus
else
pyatspidir = $(pythondir)/pyatspi
endif

pyatspi_PYTHON = \
		Accessibility.py	\
		accessible.py		\
                appevent.py             \
		application.py		\
                cache.py                \
		constants.py		\
		deviceevent.py		\
                enum.py                 \
                exceptions.py           \
		factory.py		\
		__init__.py		\
	document.py \
		interfaces.py		\
		registry.py		\
		role.py			\
		state.py		\
	text.py \
		utils.py

CLEANFILES = *.pyc
