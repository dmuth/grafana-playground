#!/bin/bash
#
# Our entrypoint script.
#

# Errors are fatal
set -e

# Make sure our log directory exists
mkdir -p /logs/septa/

#sleep 999999 # Debugging
exec /get-train-data.py

