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
		interfaces.py		\
		registry.py		\
		relation.py		\
		role.py			\
		state.py		\
		utils.py

CLEANFILES = *.pyc
