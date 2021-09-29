#!/bin/bash
#
# This script imports our data sources and dashboards and basically configures
# our Grafana container.
#

# Errors are fatal
set -e


if test ! "$1"
then
	echo "! "
	echo "! Syntax: $0 api-key"
	echo "! "
	echo "! api-key - An API key for Grafana that should have admin access."
	echo "! "
	exit 1
fi

API_KEY=$1

echo "# "
echo "# Setting up Loki and Prometheus data sources..."
echo "# "
/mnt/bin/manage-data-sources.py --api-key ${API_KEY}

echo "# "
echo "# Importing dashboards..."
echo "# "
/mnt/bin/manage-dashboards.py --api-key ${API_KEY} --import < /mnt/config/dashboards.json


