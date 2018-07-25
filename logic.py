#!/usr/bin/python3
from datetime import datetime

DATE_FORMATS = [
	('%b %d %H:%M:%S:%f %z', [25, 28]),
	('[%b %d %H:%M:%S:%f %z]', [27, 30]),
	('%m/%d/%y %H:%M:%S:%f %z', [28, 30]),
	('[%m/%d/%y %H:%M:%S:%f %z]', [30, 32]),
]

def sanitized(string):
	string = string.replace('<', '&lt;')
	string = string.replace(">", "&gt;")
	return string

def parseDate(log):

	print("Input", log)
	for (date_format, lengths) in DATE_FORMATS:
		for length in lengths:
			try:
				timestamp = datetime.strptime(log[:length], date_format)
				return (timestamp, length)
			except ValueError:
				pass
	return None

def stampedFile(originalFile):

	#	Returns: [Standard Timestamp, Remaining line, mode]
	# 	Mode: 0 or 1 if timestamp was modified or added based on previous line

	lines = originalFile.readlines()
	stampedFile = []
	minStamp = None
	for line in lines:
		parsedLog = parseDate(line)
		if parsedLog:
			timestamp, length = parsedLog
			if minStamp == None:
				minStamp = timestamp
			minStamp = max(minStamp, timestamp)
			stampedFile.append([str(timestamp), sanitized(line[length:-1]), '0'])
		else:
			stampedFile.append([str(minStamp), " " + sanitized(line[:-1]), '1'])
	return stampedFile