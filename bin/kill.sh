#!/bin/bash
#
# Kill and remove all the containers.
#

# Errors are fatal
set -e


#
# Change to the parent directory of this script.
#
pushd $(dirname $0)/.. > /dev/null

docker-compose kill
docker-compose rm -f

echo "# Done!"


