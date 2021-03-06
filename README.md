# LogSync

A tool to synchronize and compare logs generated in different timezones, with clock skews, and different timestamp formats.

# Information

This app runs on Python 3. It will not run with Python 2.7 versions due to the differences in the `datetime` objects across Python versions.

# Setup

```sh
git clone git@github.com:TheGarvitGupta/LogSync.git
```

* Download the latest version of Python 3 (https://www.python.org/downloads/)
* Installation and execution. See Setup with virual environment (Recommended).

```sh
cd LogSync
pip install -r requirements.txt
FLASK_APP=engine.py flask run
```

If you want to run it on a port other than the default (5000) port, use:
```FLASK_APP=engine.py FLASK_RUN_PORT=5001 flask run```

The tool should be accessible at `localhost:5000/`

# Setup with a virtual environment (Python3)

```sh
cd LogSync
mkdir env
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
FLASK_APP=engine.py flask run
```

# Custom Time Format

The following files contain the date formats for parsing and rendering each log file. You might need to modify these based on your log files.

`Config/date_formats.txt`: These are the formats that are (by default) used to attempt to parse the time, along with the lengths that are tried for each format.
```py
[	
	('%m/%d/%y %H:%M:%S:%f %z', [31, 28]),
	('%b %d %H:%M:%S:%f %z', [28, 25]),
	('%m/%d/%y %H:%M:%S:%f', [24, 21]),
]
```

`Config/date_print_formats.txt`: This is the default print format
```sh
"%Y/%m/%d %H:%M:%S:%f"
```
Check the `datetime` directives for understanding what those symbols mean: (https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)

# Python dependencies 

`click==6.7`
`Flask==1.0.2`
`itsdangerous==0.24`
`Jinja2==2.10`
`MarkupSafe==1.0`
`python-dateutil==2.7.3`
`pytz==2018.5`
`six==1.11.0`
`Werkzeug==0.14.1`

# Screenshots

![LogSync](https://raw.githubusercontent.com/TheGarvitGupta/LogSync/master/Screenshots/Screen%20Shot%202018-07-27%20at%203.50.05%20PM.png "LogSync")
Loaded one log with parsed timestamps, and filtering (regex)

![LogSync](https://raw.githubusercontent.com/TheGarvitGupta/LogSync/master/Screenshots/Screen%20Shot%202018-07-27%20at%203.52.18%20PM.png "LogSync")
Comparing two logs side by side

![LogSync](https://raw.githubusercontent.com/TheGarvitGupta/LogSync/master/Screenshots/Screen%20Shot%202018-07-27%20at%203.57.08%20PM.png "LogSync")
Comparing two logs by accounting for the offset in the time
