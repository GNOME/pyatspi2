testrunner_conf = configuration_data()
testrunner_conf.set('PYTHON', python3.full_path())
configure_file(input: 'testrunner.in',
               output: 'testrunner',
               configuration: testrunner_conf)

test('pyatspi', files('runtests.sh'), timeout: 300,
  env: [
    'top_srcdir=@0@'.format(meson.global_source_root()),
    'top_builddir=@0@'.format(meson.global_build_root())
  ]
)
