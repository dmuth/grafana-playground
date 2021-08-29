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
	echo "! Syntax: $0 query [ limit ] "
	echo "! "
	echo "! query - Loki query"
	echo "! limit - Limit the number of results"
	echo "! "
	exit 1
fi

QUERY=$1
LIMIT=$2

CMD="curl -G -s ${URL} --data-urlencode query=${QUERY}"

#echo "# Query: ${QUERY}"
if test "${LIMIT}"
then
	CMD="${CMD} --data-urlencode" 
	CMD="${CMD} limit=${LIMIT}"
	#echo "# Limit: ${LIMIT}"
fi

#echo $CMD; exit 1; # Debugging
${CMD}



