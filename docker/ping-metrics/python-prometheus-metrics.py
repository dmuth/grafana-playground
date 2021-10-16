#!/usr/bin/env python3
#
# Export metrics for Prometheus
#

import glob
import random
import re
import os
import time

import prometheus_client as prom

log_dir = "/logs/ping/"


#
# Return an iteratable which simulates tail -f functionality on a file, in that
# all new lines written to that file are read, and if the file is removed and 
# a new one created in its place, lines written to the new file will be read.
#
def tail_f(filename):

	seeked = False
	inode = 0

	while True:

		try:
			with open(filename) as input:

				data = os.stat(filename)
				inode = data.st_ino

				#
				# Open our file and seek to the end.
				#
				print(f"Opened file {filename}...") # Debugging
				if not seeked:
					input.seek(0, 2)
					#print(f"SEEK to end of {filename}") # Debugging
					seeked = True

				data = ""
				while True:

					data = input.read()
					#print(f"READ {len(data)} bytes!") if len(data) else False # Debugging
					#print("LATEST DATA", data) # Debugging

					if "\n" not in data:
						yield ""

						if not os.path.isfile(filename):
							print(f"FILE {filename} not found, breaking out of inner loop!") # Debugging
							break

						#
						# Okay, the file exists, but let's see if the inode changed, which can
						# happen with file rotation.  If it did, set seeked to true and break out
						# of this loop, which will cause the (new) file to be read from the beginning.
						#
						data = os.stat(filename)
						if data.st_ino != inode:
							inode = data.st_ino
							seeked = True
							break

						# We got nothing, so loop again.
						continue

					#
					# Split on newlines, and if what we have in our buffer doesn't end with a newline,
					# that means it's a partial line, and we should take the last element of the array
					# and place it back into the buffer.
					#
					lines = data.split("\n")
					if data[-1] != '\n':
						print(f"Taking partial line and putting it back into buffer...") # Debugging
						data = lines[-1]

					# Now yield each of our lines
					for line in lines[:-1]:
						yield line

		except IOError as e:
			print("Caught IOError", e)
			#
			# Set this to true, because if the file doesn't exist on the first loop, 
			# when the file (eventually?) shows up, we want to start reading from the 
			# beginning, as it'll be all new data.
			#
			seeked = True
			yield ""


#
# Parse a line and extract key=value pairs to be returned.
#
def getValues(line):

	retval = {}

	#
	# Short-circuit if this line is unparseable.
	#
	if "target=" not in line:
		return(retval)

	#
	# Filter out everything before our first key=value pair and split 
	# the rest of the line on spaces.
	#
	values = re.sub(r'.* target=', 'target=', line).split(" ")

	#
	# Loop through all key/value arrays and put them into our return value.
	# "ms" is hanging on the end as it is seprated by a space, and we can just
	# discard it as don't need it anyway.
	#
	for value in values:

		row = value.split("=")
		if row[0] == "ms":
			continue

		retval[row[0]] = row[1]
		
	return(retval)


#
# Return a list of filenames from our log directory.
#
def getFilenames(log_dir):

	retval = glob.glob(f"{log_dir}/*.log")
	return(retval)


#
# Our main entry point
#
def main(log_dir):

	filenames = getFilenames(log_dir)

	ping = prom.Summary("ping", "Pinging a host", ["host", "type"])

	#
	# Open our files for reading.
	#
	readers = []
	#filenames = [ "/logs/ping/8.8.8.8.log" ] # Debugging
	#filenames = [ "/test.log" ] # Debugging
	for filename in filenames:
		readers.append(tail_f(filename))

	prom.start_http_server(8080)
	while True:

		for reader in readers:	

			while True:

				line = next(reader)
				if line:
					data = getValues(line)
					#print("VALUES", data) # Debugging

					if "time" in data:
						ping.labels(data["target"], "latency").observe(float(data["time"]))

					elif "transmitted" in data:
						transmitted = int(data["transmitted"])
						received = int(data["received"])
						#received = int(random.randint(0, 10)) + 1 # Debugging - introduce packet loss
						#received = int(random.randint(8, 9)) + 1 # Debugging - introduce packet loss 10-20%
						#received = 9 # Debugging - introduce packet loss
						packet_loss = 100 - ( ( received / transmitted ) * 100 )
						ping.labels(data["target"], "sent").observe(transmitted)
						ping.labels(data["target"], "received").observe(received)
						ping.labels(data["target"], "packet_loss").observe(packet_loss)

					else:
						print(f"Couldn't parse line: {line}")

					continue

				#print("NEXT FILE!") # Debugging
				break

		time.sleep(1)


if __name__ == "__main__":
	main(log_dir)



