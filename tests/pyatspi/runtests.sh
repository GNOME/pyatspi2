#!/bin/sh

export PYTHONPATH=$top_srcdir:$top_srcdir/tests/pyatspi

export TEST_DATA_DIRECTORY=$top_srcdir/tests/data
export TEST_ATSPI_LIBRARY=$gtk_module_dir/libatk-bridge.so
export TEST_MODULES_DIRECTORY=$top_builddir/tests/apps
export TEST_APPLICATION=$top_builddir/tests/apps/test-application

run()
{
  chmod a+x $top_builddir/tests/pyatspi/testrunner
  $top_builddir/tests/pyatspi/testrunner -l $1 -m $2 -n $3
  result=$?
  if [ $result -ne 0 ]; then
    ret=$result
    fi
}

ret=0
run libaccessibleapp.so accessibletest AccessibleTest
run libactionapp.so actiontest ActionTest
run libaccessibleapp.so collectiontest AccessibleTest
run libcomponentapp.so componenttest ComponentTest
run librelationapp.so relationtest RelationTest
run libaccessibleapp.so statetest StateTest
exit $ret
