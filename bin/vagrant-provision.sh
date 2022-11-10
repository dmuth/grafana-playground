#!/bin/bash
#
# Set up our Vagrant instance.
#

# Errors are fatal
set -e 

apt update

apt install -y docker.io docker-compose

docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

