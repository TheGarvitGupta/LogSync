#!/usr/local/bin/python3
from flask import Flask
from dateutil import parser
from logic import stampedFile

# rgb(116, 112, 94)

app = Flask(__name__)

def file(path):
	return open(path).read()

@app.route("/")
def home():
	return file("HTML/index.html")

@app.route("/fetchLog/<file_path>")
def fetchLog(file_path):

	F = open(file_path, "r")
	StampedFile = stampedFile(F)

	fileHTML = ""

	fileHTML += "<div class='file'>"
	index = 1

	for time, line, mode in StampedFile:
		lineHTML = "<div class='line'>"
		lineHTML += "<span class='index'>" + str(index) + "\t</span>" + "<span class='timestamp'>" + time + "</span>" + "<span class='logline'>" + line + "</span>"
		lineHTML += "</div>"
		fileHTML += lineHTML
		index += 1

	return fileHTML