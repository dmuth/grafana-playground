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
echo "# Press ctrl-C to stop at anytime..."
echo "# "

rm -f ${LOG}

NUM=0
while true
do
	LINE="$(date) ${HOSTNAME} synthetic_data=true, message=${NUM}"
	echo $LINE >> ${LOG}
	NUM=$(( NUM += 1 ))
	#ls -l ${LOG} # Debugging
	sleep 1
done


