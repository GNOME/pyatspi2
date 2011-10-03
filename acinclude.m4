#######################
# type alignment test #
#######################

AC_DEFUN([DBIND_CHECK_ALIGNOF],
	[changequote(<<, >>)dnl
	dnl The name to #define.
	define(<<AC_TYPE_NAME>>,
		translit(dbind_alignof_$1, [a-z *], [A-Z_P]))dnl
	dnl The cache variable name.
	define(<<AC_CV_NAME>>,
		translit(ac_cv_alignof_$1, [ *], [_p]))dnl
	changequote([, ])dnl
	AC_MSG_CHECKING(alignment of $1)
	AC_CACHE_VAL(AC_CV_NAME,
		[AC_TRY_RUN(
			[ #include <stdio.h>
                          #include <stdlib.h>
                          #define DBUS_API_SUBJECT_TO_CHANGE
			  #include <dbus/dbus.h>
			typedef struct {char s1;} dbind_struct;
			typedef void *dbind_pointer;
			struct test {char s1; $1 s2;};
			main()
			{
			FILE *f=fopen("conftestval", "w");
			if (!f) exit(1);
			fprintf(f, "%d\n", &(((struct test*)0)->s2));
			exit(0);
			} ],
			AC_CV_NAME=`cat conftestval`,
			AC_CV_NAME=0, AC_CV_NAME=0)
		])dnl
	AC_MSG_RESULT($AC_CV_NAME)
	if test "$AC_CV_NAME" = "0" ; then
		AC_MSG_ERROR([Failed to find alignment. Check config.log for details.])
	fi
	AC_TYPE_NAME=$AC_CV_NAME
	AC_SUBST(AC_TYPE_NAME)
	undefine([AC_TYPE_NAME])dnl
	undefine([AC_CV_NAME])dnl
])

dnl AM_CHECK_PYMOD(MODNAME [,SYMBOL [,ACTION-IF-FOUND [,ACTION-IF-NOT-FOUND]]])
dnl Check if a module containing a given symbol is visible to python.
AC_DEFUN([AM_CHECK_PYMOD],
[AC_REQUIRE([AM_PATH_PYTHON])
py_mod_var=`echo $1['_']$2 | sed 'y%./+-%__p_%'`
AC_MSG_CHECKING(for ifelse([$2],[],,[$2 in ])python module $1)
AC_CACHE_VAL(py_cv_mod_$py_mod_var, [
ifelse([$2],[], [prog="
import sys
try:
	import $1
except ImportError:
	sys.exit(1)
except:
	sys.exit(0)
sys.exit(0)"], [prog="
import $1
import $1.$2"])
if $PYTHON -c "$prog" 1>&AC_FD_CC 2>&AC_FD_CC
  then
    eval "py_cv_mod_$py_mod_var=yes"
  else
    eval "py_cv_mod_$py_mod_var=no"
  fi
])
py_val=`eval "echo \`echo '$py_cv_mod_'$py_mod_var\`"`
if test "x$py_val" != xno; then
  AC_MSG_RESULT(yes)
  ifelse([$3], [],, [$3
])dnl
else
  AC_MSG_RESULT(no)
  ifelse([$4], [],, [$4
])dnl
fi
])
