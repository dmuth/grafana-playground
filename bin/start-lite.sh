#!/bin/bash
#
# Start all the containers
#

# Errors are fatal
set -e


#
# Change to the parent directory of this script.
#
pushd $(dirname $0)/.. > /dev/null

CONTAINERS="grafana loki ping ping-metrics promtail tools"

echo "# "
echo "# Starting up just the following containers:"
echo "# "
echo "# ${CONTAINERS}"
echo "# "

docker-compose up -d ${CONTAINERS}


