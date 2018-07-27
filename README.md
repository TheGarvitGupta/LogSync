# LogSync

A tool to synchronize and compare logs generated in different timezones, with clock skews, and different timestamp formats.

# Information

This app runs on Python 3. It will not run with Python 2.7 versions due to the differences in the `datetime` objects across Python versions.

# Setup

```sh
git pull git@github.com:TheGarvitGupta/LogSync.git
```

* Download the latest version of Python 3 (https://www.python.org/downloads/)
* If you would like to (highly recommended) keep the environment separate, perform the following steps in a virtual environment (https://docs.python-guide.org/dev/virtualenvs/)

```sh
cd LogSync
pip install -r requirements.txt
FLASK_APP=engine.py flask run
```

The tool should be accessible at `localhost:5000/`

# Setup with a virtual environment (Python3)

```
cd LogSync
mkdir env
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
FLASK_APP=engine.py flask run
```

# Custom Time Format

The following file contain the date formats for parsing the file and rendering finally. You might need to modify these based on your log files.

`Config/date_formats.txt`: These are the formats that are (by default) used to attempt to parse the time, along with the lengths that are tired for each format.
```
[
	('%b %d %H:%M:%S:%f %z', [25, 28]),
	('[%b %d %H:%M:%S:%f %z]', [27, 30]),
	('%m/%d/%y %H:%M:%S:%f %z', [28, 30]),
	('[%m/%d/%y %H:%M:%S:%f %z]', [30, 32]),
]
```

`Config/date_print_formats.txt`: This is the default print format
```
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
