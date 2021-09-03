#!/bin/bash
#
# This script creates and populates logfiles
#

# Errors are fatal
set -e

#LOG=logs/for-promtail.log
#LOG=/var/log/for-promtail.log
#LOG=./for-promtail.log
LOG=/var/log/promtail/for-promtail.log
CURRENT_USER=${USER}

# Change to parent directory of this script
pushd $(dirname $0)/.. > /dev/null


#
# How often to remove the file and start over?
#
RM_EVERY=1000000
#RM_EVERY=5 # Debugging


#
# Print our syntax and exit.
#
function print_syntax() {
	echo "! "
	echo "! Syntax: $0 [ truncate ] "
	echo "! "
	echo "! truncate - If specified, truncate the log."
	echo "! "
	exit 1
}


if test "$1" == "-h" -o "$1" == "---help"
then
	print_syntax
fi


if test "$1" == "truncate"
then
	echo "# "
	echo "# Truncating logfile: "
	echo "# "
	echo "# - ${LOG}"
	echo "# "
	echo > ${LOG} 
	echo "# Logs truncated!"
	exit

elif test "$1"
then
	print_syntax

fi


echo "# "
echo "# Now writing regular lines to this file: "
echo "# "
echo "# - ${LOG}"
echo "# "
echo "# Removing file every ${RM_EVERY} lines."
echo "# "
echo "# Press ctrl-C to stop at anytime..."
echo "# "

rm -f ${LOG}


NUM=0
while true
do

	NUM_1000=${NUM}
	if (( ${NUM_1000} % 1000 == 0 ))
	#if (( ${NUM_1000} % 10 == 0 )) # Debugging
	then
		NUM_1000=0
	fi

	NUM_10000=${NUM}
	if (( ${NUM_10000} % 10000 == 0 ))
	then
		NUM_10000=0
	fi

	LINE="$(date) ${HOSTNAME} synthetic_data=true, count=${NUM} count2=${NUM_1000} count3=${NUM_10000}"

	echo $LINE # Debugging
	echo $LINE >> ${LOG}

	NUM=$(( NUM += 1 ))
	#ls -l ${LOG} # Debugging
	
	#
	# When rotating the logfile, we need to rename it, as it appears that promtail
	# does not hang onto the inode if a file is deleted/overwritten, 
	# which would cause data loss. :-/
	#
	if (( ${NUM} >= ${RM_EVERY} ))
	then
		echo "# ${NUM} >= ${RM_EVERY}, removing the logfile!"
		mv -v ${LOG} ${LOG}.OLD
		NUM=0
		#ls -l $(dirname ${LOG}) || true # Debugging
	fi

	sleep 1

done


