test_bin = executable('test-application', ['test-application.c'],
                      include_directories: root_inc,
               dependencies: [ atk_dep, atspi_dep, atk_bridge_dep, gmodule_dep, dummyatk_dep, libdbus_dep])

shared_library('accessibleapp',
               ['accessible-app.c', 'atk-object-xml-loader.c'],
               include_directories: root_inc,
                 link_args: ['-Wl,--no-undefined', '-Wl,--rpath', '-Wl,/a/fake/path'],
                 dependencies: [ atk_dep, gmodule_dep, dummyatk_dep, libxml_dep])

additional_test_libs = [
  [ 'noopapp', [ 'noop-app.c' ]],
  [ 'componentapp', [ 'component-app.c' ]],
  [ 'actionapp', [ 'action-app.c' ]],
  [ 'relationapp', [ 'relation-app.c' ]]
]

foreach l: additional_test_libs
  lib = l[0]
  src = l[1]
  shared_library(lib, src, include_directories: root_inc,
                 link_args: ['-Wl,--no-undefined', '-Wl,--rpath', '-Wl,/a/fake/path'],
                 dependencies: [ atk_dep, gmodule_dep, dummyatk_dep])
endforeach
