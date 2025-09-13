project('pyatspi', 'c',
  version: '2.58.0',
  meson_version: '>= 0.46.0'
)

# Dependencies
libdbus_req_version = '>= 1.0'
glib_req_version = '>= 2.36.0'
atspi_req_version = '>= 2.46.0'
libxml_req_version = '>= 2.0.0'
pygobject_req_version = '>= 2.90.1'

python = import('python')
python3 = python.find_installation('python3', required: true)

if get_option('enable_tests')
  python.find_installation('python3', modules:['dbus'])
  libdbus_dep = dependency('dbus-1', version: libdbus_req_version)
  glib_dep = dependency('glib-2.0', version: glib_req_version)
  gobject_dep = dependency('gobject-2.0', version: glib_req_version)
  gmodule_dep = dependency('gmodule-2.0', version: glib_req_version)
  atspi_dep = dependency('atspi-2', version: atspi_req_version)
  atk_dep = dependency('atk', version: atspi_req_version)
  atk_bridge_dep = dependency('atk-bridge-2.0', version: atspi_req_version)
  libxml_dep = dependency('libxml-2.0', version: libxml_req_version)
endif

pygobject_dep = dependency('pygobject-3.0', version: pygobject_req_version)

root_inc = include_directories('.')

subdir('pyatspi')

if get_option('enable_tests')
  subdir('tests')
endif
