from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():

	content = []
	for i in range(0, 5):
		F = open("log.log", "r")
		read = F.readlines()
		content.extend(read)

	print(len(content))

	return "<style> body {font-family: Menlo Regular, Monospace, Consolas; background-color: rgb(40, 41, 35); color: rgb(248, 248, 242);} </style>" + "<br>".join(content)