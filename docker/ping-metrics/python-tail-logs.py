#!/usr/bin/env python3
#
# This script will mimic tail -f functionality in Python.
# It will correctly handle files that haven't been created yet, as well as files that are removed.
#
# It is based heavily on an example I found at:
#		https://newbedev.com/how-can-i-tail-a-log-file-in-python
#
# However, I did some optimization. :-)
# 
#
# NOTE: If you are running this in Docker on a Mac (as I do), don't create test files in MacOS, 
# create them in Docker.  Otherwise you're gonna have really weird filesystem caching issues.
#


import time
import os


def tail_f(filename):

	seeked = False

	while True:

		try:
			with open(filename) as input:

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


def main(filename):

	readers = []
	for filename in filename:
		readers.append(tail_f(filename))

	while True:

		for reader in readers:	

			while True:

				line = next(reader)
				if line:
					print(line)
					continue

				#print("NEXT FILE!") # Debugging
				break

		# If we made it here, no line was read, sleep for a bit.
		#print("SLEEPING") # Debugging
		time.sleep(1)
			

filenames = [
	"/logs/ping/google.com.log",
	"/logs/ping/8.8.8.8.log"
	]
filenames = ["/mnt/test.log"]
main(filenames)


