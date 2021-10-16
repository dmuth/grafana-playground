#!/bin/bash
#
# Our entrypoint script.
#

# Errors are fatal
set -e


#
# If we didn't get arguments, do default behavior.
#
if test ! "$1"
then

	#sleep 999999 # Debugging
  /python-prometheus-metrics.py
	exit

fi


#
# If we got arguments, run them.
#
exec $@

