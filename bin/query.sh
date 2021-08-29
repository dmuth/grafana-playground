#!/bin/bash
#
# Query Loki
#

# Errors are fatal
set -e

URL="http://localhost:3100/loki/api/v1/query"

if test ! "$1"
then
	echo "! "
	echo "! Syntax: $0 query"
	echo "! "
	echo "! query - Loki query"
	echo "! "
	exit 1
fi

curl -G -s ${URL} --data-urlencode $@


