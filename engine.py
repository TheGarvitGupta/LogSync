#!/usr/local/bin/python3
from flask import Flask, request, send_from_directory, redirect
from dateutil import parser
from datetime import timedelta
from logic import stampedFile, fileName, stringTime, updateDeltaFiles, interleave
import urllib
import random

zeroDelta = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
LOG_FILES = {}
FILE_DELTAS = {}
DELTA_FILES = {}

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
	print("Delta:", delta)
	FILE_DELTAS[filePath] = (input_delta, delta)

	global DELTA_FILES
	if delta == zeroDelta:
		print("Updating to zero delta")
		DELTA_FILES[filePath] = LOG_FILES[filePath]
	else:
		DELTA_FILES = updateDeltaFiles(LOG_FILES, FILE_DELTAS)

	return redirect("/", code=302)

@app.route('/addLog/<path:file_path>')
def addLog(file_path):
	print("Searching for", file_path)
	try:
		F = open(file_path, "r")
	except(FileNotFoundError):
		try:
			F = open("/" + file_path, "r")
		except(FileNotFoundError):
			return errorMessage("-ERR: Could not open file " + file_path)
	StampedFile = stampedFile(F)
	LOG_FILES[file_path] = StampedFile
	FILE_DELTAS[file_path] = ((0,0,0,0,0,0,0), timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))
	DELTA_FILES[file_path] = LOG_FILES[file_path]
	return "+OK: Loaded file " + file_path

@app.route('/renderTimeline')
def renderTimeline():
	return renderPane()

def renderPane():
	logHTMLS = []
 
	SPARCE_LOG = interleave(DELTA_FILES)

	logs = len(SPARCE_LOG)
	for filePath in SPARCE_LOG:
		StampedFile = SPARCE_LOG[filePath]
		fileHTML = "<div class='file" + " div-"+ str(logs) + "'>"
		fileHTML += "	<div class='file-menu'>"
		fileHTML += "		<div class='file-name' title='" + filePath+ "'>" + fileName(filePath) + "</div>"
		fileHTML += "		<form class='deltas-form' action='updateDeltas'>"

		((y,m,d,H,M,S,f), delta) = FILE_DELTAS[filePath]
		fileHTML += "		<input style='display:none' name='filePath' type='text' value='" + filePath + "'>"
		fileHTML += "		<div class='label-delta label-y'><input class='time-delta delta-y td-left' name='y' type='text' value='" + str(y) + "' placeholder='Years'></div>"
		fileHTML += "		<div class='label-delta label-m'><input class='time-delta delta-m' name='m' type='text' value='" + str(m) + "' placeholder='Months '></div>"
		fileHTML += "		<div class='label-delta label-d'><input class='time-delta delta-d' name='d' type='text' value='" + str(d) + "' placeholder='Days'></div>"
		fileHTML += "		<div class='label-delta label-H'><input class='time-delta delta-H' name='H' type='text' value='" + str(H) + "' placeholder='Hours'></div>"
		fileHTML += "		<div class='label-delta label-M'><input class='time-delta delta-M' name='M' type='text' value='" + str(M) + "' placeholder='Minutes'></div>"
		fileHTML += "		<div class='label-delta label-S'><input class='time-delta delta-S' name='S' type='text' value='" + str(S) + "' placeholder='Seconds'></div>"
		fileHTML += "		<div class='label-delta label-f'><input class='time-delta delta-f td-right' name='f' type='text' value='" + str(f) + "' placeholder='Microseconds'></div>"
		fileHTML += "		<input class='time-delta delta-button' type='submit' value='Update'>"

		fileHTML += "		</form>"
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

