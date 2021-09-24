#!/usr/bin/env python3
#
# This script lets us add data sources to Grafana
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

	args = parser.parse_args()
	return(args)


#
# Wrapper to print a string to stderr.
#
def stderr(string):
		print(string, file=sys.stderr)


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
# Add a specific data source.
#
def add_data_source(api_url, api_key, name, source_type, target_url, default = False):

	headers = {
		"Content-Type":"application/json",
		"Accept": "application/json",
    "Authorization": f"Bearer {api_key}",
	}
	url_import = f"{api_url}/api/datasources"

	data = {
  	"name": name,
		"type": source_type,
  	"url": target_url,
		"access":"proxy",
		"basicAuth": False,
	}

	if default:
		data["isDefault"] = True

	r = requests.post(url = url_import, headers = headers, data = json.dumps(data))

	stderr(f"Adding data source {name} with URL {target_url}...")

	if r.status_code == 409:
		stderr("That data source already exists, skipping!")

	elif r.status_code != 200:
		raise Exception(f"Status code {r.status_code} != 200 for URL '{url_import}'!  Message returned: {r.text}")


#
# Add our data sources.
#
def add_data_sources(url, api_key):

	add_data_source(url, api_key, "Loki", "loki", "http://loki:3100", default = True)
	add_data_source(url, api_key, "Prometheus", "prometheus", "http://prometheus:9090")


#
# Our main entrypoint.
#
def main():

	args = getArgs()
	#print(args) # Debug

	# Double-slashes don't play nice with Grafana.
	url = args.url.rstrip("/")

	add_data_sources(url, args.api_key)


main()


