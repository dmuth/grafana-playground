#!/bin/bash
#
# This script watches storage usage of the Loki database
#

# Fail with error status if a command fails.
set -e

# Change to the parent directory of this script
pushd $(dirname $0)/.. > /dev/null

DIR="data"
DIR_DATA="${DIR}/loki-data"
DIR_WAL="${DIR}/loki-wal"


ls -l ${DIR_DATA}/chunks | wc -l; echo
find ${DIR_DATA} -type f | head | xargs ls -lh; echo
find ${DIR_WAL} -type f | head | xargs ls -lh



