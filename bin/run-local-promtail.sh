#!/bin/bash
#
# Run the local instance of Promtail.
# If you're on a Mac, you'll HAVE to use this to ingest /var/log/, as it is not 
# exported to Docker for Mac, probably due to the System Integrity Protection of OS/X.
#

# Errors are fatal
set -e

CONFIG=./config/promtail-config-local.yaml

# Change to parent directory of this script
pushd $(dirname $0)/.. > /dev/null


promtail -config.file ${CONFIG}



