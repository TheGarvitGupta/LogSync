#!/usr/local/bin/python3
from flask import Flask, request, send_from_directory, redirect
from dateutil import parser
from datetime import timedelta
from logic import stampedFile, fileName, stringTime, updateDeltaFiles, interleave, applyFilters, matches, validateFile	
import urllib
import random, re

zeroDelta = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
LOG_FILES = {}
FILE_DELTAS = {}
DELTA_FILES = {}
FILE_FILTERS = {}

app = Flask(__name__)

@app.route("/")
def home():
	return send_from_directory("", "HTML/index.html")

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('HTML/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('HTML/css', path)

@app.route('/updateDeltas', methods=['GET'])
def updateDeltas():
	filePath = request.args.get('filePath')
	y = int(float(request.args.get('y'))) if request.args.get('y') else 0
	m = int(float(request.args.get('m'))) if request.args.get('m') else 0
	d = int(float(request.args.get('d'))) if request.args.get('d') else 0
	H = int(float(request.args.get('H'))) if request.args.get('H') else 0
	M = int(float(request.args.get('M'))) if request.args.get('M') else 0
	S = int(float(request.args.get('S'))) if request.args.get('S') else 0
	f = int(float(request.args.get('f'))) if request.args.get('f') else 0

	input_delta = (y,m,d,H,M,S,f)
	delta = timedelta(days=y*365 + m*30 + d, seconds=S, microseconds=f, minutes=M, hours=H)
	FILE_DELTAS[filePath] = (input_delta, delta)

	global DELTA_FILES
	if delta == zeroDelta:
		DELTA_FILES[filePath] = LOG_FILES[filePath]
	else:
		DELTA_FILES = updateDeltaFiles(LOG_FILES, FILE_DELTAS)

	return redirect("/", code=302)

@app.route('/filter', methods=['GET'])
def filter():
	filePath = request.args.get('filePath')
	value = request.args.get('value')

	print("Filter received", filePath, value)

	try:
		re.compile(value)
	except re.error:
		return "-ERR: " + value + " is not a valid regular expression"
	FILE_FILTERS[filePath] = value

	if value == "":
		return "+OK: " + fileName(filePath) + " restored"

	match = matches(value, ''.join(str(r) for v in LOG_FILES[filePath] for r in v))
	return "+OK: Applied '" + value + "' to " + fileName(filePath) + " [" + str(match) + " matches]"

@app.route('/remove/<path:path>')
def remove(path):
	LOG_FILES.pop(path, None)
	FILE_DELTAS.pop(path, None)
	DELTA_FILES.pop(path, None)
	return redirect("/", code=302)

@app.route('/addLog/<path:file_path>')
def addLog(file_path):
	try:
		F = open(file_path, "r")
	except(FileNotFoundError):
		try:
			F = open("/" + file_path, "r")
		except(FileNotFoundError):
			return "-ERR: Could not open file " + file_path

	if file_path in LOG_FILES:
		return "-ERR: " + fileName(file_path) + " already loaded"

	StampedFile = []
	
	try:
		StampedFile = stampedFile(F)
	except(TypeError):
		return "-ERR: Could not parse " + fileName(file_path) + ". Please see ./Config/date_formats.txt to add date parsing fomats."

	if not validateFile(StampedFile):
		return "-ERR: Could not parse " + fileName(file_path) + ". Please see ./Config/date_formats.txt to add date parsing fomats."

	LOG_FILES[file_path] = StampedFile
	FILE_DELTAS[file_path] = ((0,0,0,0,0,0,0), timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))
	DELTA_FILES[file_path] = LOG_FILES[file_path]
	return "+OK: Loaded file " + fileName(file_path)

@app.route('/renderTimeline')
def renderTimeline():
	return renderPane()

def renderPane():
	logHTMLS = []

	FILTERED_DELTA_FILES = applyFilters(DELTA_FILES, FILE_FILTERS)
	SPARCE_LOG = interleave(FILTERED_DELTA_FILES)

	logs = len(SPARCE_LOG)
	for filePath in SPARCE_LOG:
		StampedFile = SPARCE_LOG[filePath]
		fileHTML = "<div class='file" + " div-"+ str(logs) + "'>"
		fileHTML += "	<div class='file-menu'>"
		fileHTML += "		<div class='file-name' title='" + filePath+ "'>" + fileName(filePath) + " [<a class='remove' href='/remove/" + filePath+ "''>remove</a>] </div>	"
		fileHTML += "		<form class='deltas-form' action='updateDeltas'>"

		((y,m,d,H,M,S,f), delta) = FILE_DELTAS[filePath]
		fileHTML += "		<input style='display:none' name='filePath' type='text' value='" + filePath + "'>"
		fileHTML += "		<div class='label-delta label-y'><input class='time-delta delta-y td-left' name='y' type='number' required value='" + str(y) + "' placeholder='Years'></div>"
		fileHTML += "		<div class='label-delta label-m'><input class='time-delta delta-m' name='m' type='number' required value='" + str(m) + "' placeholder='Months '></div>"
		fileHTML += "		<div class='label-delta label-d'><input class='time-delta delta-d' name='d' type='number' required value='" + str(d) + "' placeholder='Days'></div>"
		fileHTML += "		<div class='label-delta label-H'><input class='time-delta delta-H' name='H' type='number' required value='" + str(H) + "' placeholder='Hours'></div>"
		fileHTML += "		<div class='label-delta label-M'><input class='time-delta delta-M' name='M' type='number' required value='" + str(M) + "' placeholder='Minutes'></div>"
		fileHTML += "		<div class='label-delta label-S'><input class='time-delta delta-S' name='S' type='number' required value='" + str(S) + "' placeholder='Seconds'></div>"
		fileHTML += "		<div class='label-delta label-f'><input class='time-delta delta-f td-right' name='f' type='number' value='" + str(f) + "' placeholder='Microseconds'></div>"
		fileHTML += "		<input class='time-delta delta-button' type='submit' value='Update'>"

		fileHTML += "		</form>"

		fileFilter = FILE_FILTERS[filePath] if filePath in FILE_FILTERS else ""

		fileHTML += "		<span class='grep'><input class='regex' name='" + filePath + "' value='"+ fileFilter +"' onkeyup='filter(this)' ></span>"
		fileHTML += "	</div>"

		for index, time, line, mode in StampedFile:
			lineHTML = "<div class='line'>"
			if index == 0:
				lineHTML += "<span class='index'>" + "\t</span>" + "<span class='timestamp'>" + "</span>" + "<span class='logline'>" + " " + "</span>"
			else:

				if mode == '0':
					lineHTML += "<span class='index'>" + str(index) + "\t</span>" + "<span class='timestamp'>" + stringTime(time) + "</span>" + "<span class='logline'>" + line + "</span>"
				else:
					lineHTML += "<span class='index'>" + str(index) + "\t</span>" + "<span class='timestamp-interpolated'>" + stringTime(time) + "</span>" + "<span class='logline'>" + line + "</span>"
			lineHTML += "</div>"
			fileHTML += lineHTML

		fileHTML += "</div>"
		logHTMLS.append(fileHTML)

	return "".join(logHTMLS)

def errorMessage(string):
	return "<div class='error'>" + string + "</div>"

