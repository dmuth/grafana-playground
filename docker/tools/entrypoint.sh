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

	#
	# Launching this container won't do anything, but it'll be provided as a container
	# to connect to so that we can run scripts in an environment which has the 
	# appropriate Python modules loaded.
	#
	sleep 999999
	exit

fi


#
# If we got arguments, run them.
#
exec $@

