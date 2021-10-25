#!/usr/bin/env python3
#
# Read train data once per minute and write it to our logs.
#

import datetime
import json
from pathlib import Path
import time

import requests

url = "http://www3.septa.org/hackathon/TrainView/"
log = "/logs/septa/regional-rail.log"


#
# Read the train data, parse it, and return it as an array of dicts.
#
def read_url(url):

	retval = []

	r = requests.get(url)
	if r.status_code != 200:
		raise Exception(f"Status code {r.status_code} != 200")

	now = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

	for train in r.json():
		data = {}
		data["time"] = now
		data = data | train
		retval.append(data)

	return(retval)


#
# Read our SEPTA logs
#
def read_logs(url, log):

	# Rotate our logfile if it exists
	file = Path(log)
	if file.is_file():
		new = f"{log}.OLD"
		print(f"Renaming file {log} to {new}...")
		file.rename(new)

	file = open(log, "w")
	print(f"Opening file {log} for writing...")

	#
	# Exit after reading a day's worth of logs so that logfiles can be rotated
	#
	for i in range(1570):

		try:
			trains = read_url(url)
			for train in trains:
				line = json.dumps(train)
				file.write(line + "\n")

		except Exception as e:
			print("Caught Exception: ", e)

		#
		# Sleep for less than a minute so that delays don't cause a minute's worth of readings to be skipped.
		# In other words, I'd rather have an occasional duplicate reading than a missed reading.
		#
		file.flush()
		time.sleep(55)

	print(f"Done with main loop, closing file {log}...")
	file.close()

while True:
	read_logs(url, log)


