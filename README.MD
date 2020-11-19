# Automatic join tool for multiple meeting platforms

This Python-Script can be used to join Webex and Zoom meetings automatically on linux. 
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

-h: Flag if hotkeys are being used in OBS (ctrl alt s for stopping recording)

--dry: Dry run: Webex test website will open so you can configure OBS. Default duration 2 minutes

**Example:**

`./main.py -n "Your Name" -e Your@email.com  -d 90 -r -u "https://www.webex.com/de/test-meeting.html"`

**Configuration for OBS**

To use the recording feature, OBS has to be installed.
Use the script with only the --dry flag to open a Window and OBS. 
In OBS you can now select if the chromium Window or the whole screen should be used.
Use the -h flag and set ctrl alt s for stopping recording as hotkey in OBS. 
It works without if you use .mkv but .mp4 has problems without. 

**Dependencies**

Things that have to be installed:

- Open Broadcaster Software®
- chromium-chromedriver
- Python 3
- Selenium for python

**Requirements for Zoom**

This only works when zoom is installed locally.

These settings are needed:

In Zoom: Auto join meeting with audio (and maybe join mute)

in Browser: Always allow zoom.us to open links of this type (appears when joining manually)


## DISCLAIMER
There is no warranty for this software and the usage of it and its features is on your own risk.

Before using the recording feature make sure that you don't violate any laws or term of services.
