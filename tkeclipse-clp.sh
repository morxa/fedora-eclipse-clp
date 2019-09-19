#!/usr/bin/sh
ECLIPSEDIR="${ECLIPSEDIR:-/usr/libexec/eclipse-clp}"
export ECLIPSEDIR
exec /usr/libexec/eclipse-clp/lib_tcl/tkeclipse.tcl "$@"
