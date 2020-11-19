# Webex automatic join tool

This Python-Script can be used to join Webex meetings automatically on linux. 
Meetings can be automatically recorded with OBS and the join time/date can be scheduled.

## Usage
**Arguments:**

-u: Url to meeting

-n: Name to display in meeting

-e Email to display

-d: Meeting duration in minutes

-s: Schedule Time/Date DDMMYYYYHHMM of meeting

-r: Flag to start recording with OBS

-i: Set flag if link leads to meeting invite page

--dry: Dry run: Webex test website will open so you can configure OBS. Default duration 2 minutes

**Example:**

`./main.py -n "Your Name" -e Your@email.com  -d 90 -r -u "https://www.webex.com/de/test-meeting.html"`

**Configuration for OBS**

To use the recording feature, OBS has to be installed.
Use the script with only the --dry flag to open a Window and OBS. 
In OBS you can now select if the chromium Window or the whole screen should be used.

**Dependencies**

Things that have to be installed:

- Open Broadcaster Software®
- chromium-chromedriver
- Python 3
- Selenium for python

## DISCLAIMER
There is no warranty for this software and the usage of it and its features is on your own risk.

Before using the recording feature make sure that you don't violate any laws or term of services.
