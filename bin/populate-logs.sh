#!/bin/bash
#
# This script creates and populates logfiles
#

# Errors are fatal
set -e

LOG_LOCAL=/var/log/for-promtail.log
LOG_DOCKER=logs/for-dockerized-promtail.log
CURRENT_USER=${USER}

# Change to parent directory of this script
pushd $(dirname $0)/.. > /dev/null


echo "# "
echo "# Creating ${LOG_LOCAL} and changing owner to ${CURRENT_USER}..."
echo "# You may be asked for your sudo password shortly..."
echo "# "
sudo touch ${LOG_LOCAL}
sudo chown ${CURRENT_USER} ${LOG_LOCAL}

echo "# Okay, ${LOG_LOCAL} exists and is now owned by you!"

echo "# Making log directory for ${LOG_DOCKER}..."
mkdir -p $(dirname ${LOG_DOCKER})

echo "# "
echo "# Now writing regular lines to each of these files: "
echo "# "
echo "# - ${LOG_LOCAL}"
echo "# - ${LOG_DOCKER}"
echo "# "
echo "# Press ctrl-C to stop at anytime..."
echo "# "

NUM=0
while true
do
	LINE="$(date) ${HOSTNAME} synthetic data, message #${NUM}"
	echo $LINE >> ${LOG_LOCAL}
	echo $LINE >> ${LOG_DOCKER}
	NUM=$(( NUM += 1 ))
	sleep 1
done


