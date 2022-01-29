# Spond
![spond logo](https://github.com/Olen/Spond/blob/main/images/spond-logo.png?raw=true)

Simple library with some example scripts to access data from Spond.

## Usage

Unless you haven't already, install pipenv as documented [https://packaging.python.org/en/latest/tutorials/managing-dependencies/](here)

Run `pipenv install`

Rename `config.py.sample` to config.py and set your Spond username and password in that file.

Run `pipenv run python3 ical.py` which will generate an ics-file (`spond.ics`) of the upcoming events in Spond (which can then be imported into any calendar, or even put up on a web page to be subscribed to by different calendar apps.

Run `pipenv run python3 groups.py` which will simply dump all your groups and group memebers to a JSON file (`<group name>.json`)
