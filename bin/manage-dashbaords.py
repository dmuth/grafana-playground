#!/usr/bin/env python3
#
# This script lets us export and import all dashboards from our Grafana instance.
#


import argparse
import json

import requests


#
# Parse our arguments.
#
def getArgs():

	parser = argparse.ArgumentParser(description = "Export and import Grafana dashboards")
	parser.add_argument("--api-key", required = True, 
		help = "The Grafana API key.  Can be Generated in Grafana at: Configuration -> API Keys")
	parser.add_argument("--url", default ="http://localhost:3000/",
		help = "Base URL for a Grafana sever. Defaults to http://localhost:3000/")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--export", action = "store_true", help = "Export dashboards as JSON to stdout.")
	group.add_argument("--import", action = "store_true", help = "Read JSON from stdin to create dashboards.")

	args = parser.parse_args()
	return(args)


#
# Get our dashbaord IDs and return them as an array.
#
def getDashboardIds(url, headers):

	retval = []

	r = requests.get(url = url, headers = headers)
	if r.status_code != 200:
		raise Exception(f"Status code {r.status_code} != 200 for URL '{url}'!")

	for dashboard in r.json():
		retval.append(dashboard["uid"])

	return(retval)


#
# Get the data for each of our dashboards and return it in an array.
#
def getDashboards(url, headers, ids):

	retval = []

	for uid in ids:
		dashboard = getDashboard(url, headers, uid)
		retval.append(dashboard)

	return(retval)


#
# Get the data for a specific dashboard and return it in a dict.
#
def getDashboard(url, headers, uid):

	url = f"{url}/api/dashboards/uid/{uid}"
	r = requests.get(url = url, headers = headers)
	if r.status_code != 200:
		raise Exception(f"Status code {r.status_code} != 200 for URL '{url}'!")

	#
	# We don't need the meta data, just the dashboard.
	#
	return(r.json()["dashboard"])


#
# Get all of our dashboards and return them as a dictionary.
#
def export(url, api_key):

	url_search = f"{url}/api/search?query=%"
	headers = {
    "Authorization": f"Bearer {api_key}"
	}

	ids = getDashboardIds(url_search, headers)
	dashboards = getDashboards(url, headers, ids)

	return(dashboards)

#
# Our main entrypoint.
#
def main():

	args = getArgs()
	#print(args) # Debug

	# Double-slashes don't play nice with Grafana.
	url = args.url.rstrip("/")

	if args.export:
		dashboards = export(url, args.api_key)
		output = {"dashboards": dashboards}
		output["meta"] = {"app": "Grafana Playground"}
		print(json.dumps(output))

	# TODO: args.import should read JSON from stdin


main()


