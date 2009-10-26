
if RELOCATE_PYATSPI
pyatspidir = $(pythondir)/$(PYATSPI_SUBDIR)/pyatspi
else
pyatspidir = $(pythondir)/pyatspi
endif

pyatspi_PYTHON = \
		Accessibility.py	\
		accessible.py		\
		action.py		\
                appevent.py             \
		application.py		\
                cache.py                \
		collection.py		\
		component.py		\
		constants.py		\
		desktop.py		\
		deviceevent.py		\
		document.py		\
		editabletext.py		\
                enum.py                 \
                exceptions.py           \
		factory.py		\
		hyperlink.py		\
		hypertext.py		\
		image.py		\
		__init__.py		\
		interfaces.py		\
                loop.py                 \
		registry.py		\
		relation.py		\
		role.py			\
		selection.py		\
                settings.py             \
		state.py		\
		table.py		\
		text.py			\
		utils.py		\
		value.py

if RELOCATE_PYATSPI
install-exec-local: Makefile
	@$(MKDIR_P) $(DESTDIR)$(pyexecdir)
	cp pyatspi-dbus.pth $(DESTDIR)$(pyexecdir)

uninstall-local:
	@rm $(DESTDIR)$(pyexecdir)/pyatspi-dbus.pth
endif

CLEANFILES = *.pyc
