#!/usr/bin/sh
ECLIPSEDIR="${ECLIPSEDIR:-/usr/libexec/eclipse-clp}"
export ECLIPSEDIR
DAVINCIHOME="${DAVINCIHOME:-$ECLIPSEDIR/daVinci/x86_64_linux}"
export ECLIPSEDIR TCL_LIBRARY TK_LIBRARY  LD_LIBRARY_PATH DAVINCIHOME 
exec "wish" "/usr/libexec/eclipse-clp/lib_tcl/tktools.tcl" -- "$@"
