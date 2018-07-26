#!/usr/bin/python3
from datetime import datetime
from datetime import timedelta
import pytz

DATE_FORMATS = [
	('%b %d %H:%M:%S:%f %z', [25, 28]),
	('[%b %d %H:%M:%S:%f %z]', [27, 30]),
	('%m/%d/%y %H:%M:%S:%f %z', [28, 30]),
	('[%m/%d/%y %H:%M:%S:%f %z]', [30, 32]),
]

DATE_PRINT_FORMAT = "%H:%M:%S:%f"

def sanitized(string):
	string = string.replace('<', '&lt;')
	string = string.replace(">", "&gt;")
	return string

def standardDate(localDate):
	# print(localDate.utcnow)
	return localDate.astimezone(pytz.utc)

def parseDate(log):
	for (date_format, lengths) in DATE_FORMATS:
		for length in lengths:
			try:
				timestamp = datetime.strptime(log[:length], date_format)
				return (standardDate(timestamp), length)
			except ValueError:
				pass
	return None

def stringTime(datetime_):
	return datetime_.strftime(DATE_PRINT_FORMAT)

def stampedFile(originalFile):
	#	Returns: [Standard Timestamp, Remaining line, mode]
	# 	Mode: 0 or 1 if timestamp was modified or added based on previous line
	lines = originalFile.readlines()
	stampedFile = []
	minStamp = None
	index = 1
	for line in lines:
		parsedLog = parseDate(line)
		if parsedLog:
			timestamp, length = parsedLog
			if minStamp == None:
				minStamp = timestamp
			minStamp = max(minStamp, timestamp)
			stampedFile.append([index, timestamp, sanitized(line[length:-1]), '0'])
		else:
			stampedFile.append([index, minStamp, " " + sanitized(line[:-1]), '1'])
		index += 1
	return stampedFile

def updateDeltaFiles(LOG_FILES, FILE_DELTAS):
	DELTA_FILES = {}
	for file in LOG_FILES:
		DELTA_FILES[file] = []
		((y,m,d,H,M,S,f), delta) = FILE_DELTAS[file]
		for [index, timestamp, line, mode] in LOG_FILES[file]:
			DELTA_FILES[file].append([index, timestamp + delta, line, mode])
	return DELTA_FILES

def fileName(filePath):
	slash = 0
	for i in range(0, len(filePath)):
		if filePath[i] == '/':
			slash = i
	return filePath[slash + 1:]