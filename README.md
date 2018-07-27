# LogSync

A tool to synchronize and compare logs generated in different timezones, with clock skews, and different timestamp formats.

# Information

This app runs on Python 3. It will not run with Python 2.7 versions due to the differences in the `datetime` objects across Python versions.

# Setup

```sh
git pull git@github.com:TheGarvitGupta/LogSync.git
```

* Download the latest version of Python 3 (https://www.python.org/downloads/)
* If you would like to keep the environment separate, perform the follwoing steps in a virtual environment (https://docs.python-guide.org/dev/virtualenvs/)

```sh
cd LogSync
pip install -r requirements.txt
FLASK_APP=engine.py flask run
```

# Python dependencies 

