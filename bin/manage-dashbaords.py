#!/usr/bin/env python3
#
# This script lets us export and import all dashboards from our Grafana instance.
#


import argparse
import json
import sys

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
# Wrapper to print a string to stderr.
#
def stderr(string):
		print(string, file=sys.stderr)


#
# Read JSON from stdin and parse it.
#
def import_json():

	string = ""
	for line in sys.stdin:
		string += line

	data = json.loads(string)

	#
	# Check to see if we have the right meta data.
	# This is mainly a sanity check because I don't want random data being fed
	# into this and then bug reports getting triggered.
	# I *only* want data that was created by this script's export process. :-)
	#
	if "meta" in data:
		if "app" in data["meta"]:
			if data["meta"]["app"] == "Grafana Playground":
				return(data["dashboards"])
			else:
				raise Exception(f"Invalid app type '{data['meta']['app']}' in metadata, expecting 'Grafana Playground'!")
		else:
			raise Exception("Invalid metadata in export file.")
	else:
		raise Exception("Metadata not found in export file.")


#
# Go through our dashboards and import them.
#
def import_dashboards(url, api_key, dashboards):

	headers = {
    "Authorization": f"Bearer {api_key}",
		"Content-Type":"application/json",
		"Accept": "application/json"
	}
	url_import = f"{url}/api/dashboards/db"

	for dashboard in dashboards:
		new_dashboard = {"dashboard": dashboard}
		id = new_dashboard["dashboard"]["id"]
		uid = new_dashboard["dashboard"]["uid"]
		title = new_dashboard["dashboard"]["title"]
		new_dashboard["overwrite"] = True

		r = requests.post(url = url_import, headers = headers, 
			data = json.dumps(new_dashboard))
		stderr(f"Importing dashboard uid={uid} id={id} title={title}...")

		if r.status_code == 404:
			stderr(f"Dashboard uid {uid} not found, let's create it instead!")
			new_dashboard["overwrite"] = False
			new_dashboard["dashboard"]["id"] = None

			r = requests.post(url = url_import, headers = headers, 
				data = json.dumps(new_dashboard))

		elif r.status_code != 200:
			raise Exception(f"Status code {r.status_code} != 200 for URL '{url_import}'!  Message returned: {r.text}")

		stderr(f"Imported dashboard '{new_dashboard['dashboard']['title']}' " + 
				f"(uid {uid}), "
				+ f"results: {r.text}")


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

	elif args.__dict__["import"]:
		# import is a great term, but a reserved word, hence messing with __dict__...
		stderr("Now reading JSON of an export file from stdin...")
		dashboards = import_json()
		import_dashboards(url, args.api_key, dashboards)

	else:
		raise("Invalid arguments!")


main()


