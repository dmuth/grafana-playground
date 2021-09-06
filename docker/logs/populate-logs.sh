#!/bin/bash
#
# This script creates and populates logfiles
#

# Errors are fatal
set -e

LOG="/logs/synthetic/synthetic.log"
LOG_MANUAL="/logs/synthetic/manual.log"
CURRENT_USER=${USER}

# Change to parent directory of this script
pushd $(dirname $0)/.. > /dev/null

#
# How often to remove the file and start over?
#
RM_EVERY=100000
#RM_EVERY=5 # Debugging

# Ensure our log directory exists.
mkdir -p $(dirname ${LOG})


#
# Print our syntax and exit.
#
function print_syntax() {
	echo "! "
	echo "! Syntax: $0 [ num ] "
	echo "! "
	echo "! num - If specified, manually write num rows to ${LOG_MANUAL} and then exit."
	echo "! "
	exit 1
}


if test "$1" == "-h" -o "$1" == "---help"
then
	print_syntax
fi


if test "$1" 
then
	NUM_ROWS=$1
	echo "# "
	echo "# Manually feeding ${NUM_ROWS} rows into ${LOG_MANUAL}..."
	echo "# "

	if test "${NUM_ROWS}" -le 0
	then
		print_syntax
	fi

	# Cleanup from a previous run.
	rm -fv ${LOG_MANUAL} > /dev/null

	#
	# Calculate how many characters wide the numbers should be.
	# We have to do this because % will assume that numbers with leading zeros
	# are octal and choke on them.
	#
	WIDTH=$(echo -n ${NUM_ROWS} | wc -c)

	DATE=$(date)

	for I in $(seq 1 ${NUM_ROWS})
	do

		#
		# Every 100 rows, let's grab a new date. 
		# This is less abusive than running the date command on *every* row,
		# yet still lets us keep the date close to being in sync with the rows.
		#
		if (( ${I} % 100 == 0 ))
		then
			DATE=$(date)
		fi

		LINE="${DATE} ${HOSTNAME} This is manual data. count=${I} total=${NUM_ROWS}" 
		printf "%s %s This is manual data. count=%0${WIDTH}d total=%s\n" \
			"${DATE}" "${HOSTNAME}" "${I}" "${NUM_ROWS}" >> ${LOG_MANUAL}
	done

	#ls -l $(dirname ${LOG}) # Debugging

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

# Cleanup from a previous run.
rm -f ${LOG}


#
# If we made it here, we're going to do a "normal" run, wherein we loop forever,
# writing one row a second, and periodically rotating the logfile so it doesn't 
# grow too large.
#
NUM=0
NUM_1000=0
NUM_10000=0
while true
do

	if (( ${NUM_1000} % 1000 == 0 ))
	#if (( ${NUM_1000} % 10 == 0 )) # Debugging
	then
		NUM_1000=0
	fi

	if (( ${NUM_10000} % 10000 == 0 ))
	then
		NUM_10000=0
	fi

	LINE="$(date) ${HOSTNAME} This is synthetic data, beep-bep! count=${NUM} count2=${NUM_1000} count3=${NUM_10000}"

	#echo $LINE # Debugging
	echo $LINE >> ${LOG}

	NUM=$(( NUM += 1 ))
	NUM_1000=$(( NUM_1000 += 1 ))
	NUM_10000=$(( NUM_10000 += 1 ))
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


