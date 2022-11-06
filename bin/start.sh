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

docker-compose up -d


