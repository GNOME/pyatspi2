dummyatk_sources = [
  'my-atk-action.c',
  'my-atk-component.c',
  'my-atk-document.c',
  'my-atk-hyperlink.c',
  'my-atk-hypertext.c',
  'my-atk-object.c',
  'my-atk-selection.c',
  'my-atk-table.c',
  'my-atk-text.c',
  'my-atk-value.c',
  'resources_storage.c',
  'useful_functions.c',
  'user_marshal.c'
]

dummyatk = static_library('dummyatk', dummyatk_sources,
                          include_directories: root_inc,
                          dependencies: [ glib_dep, gobject_dep, atk_dep ])

dummyatk_dep = declare_dependency(link_with: dummyatk,
                                  dependencies: [ glib_dep, gobject_dep, atk_dep ],
                                  include_directories: include_directories('.'))
