#!/usr/local/bin/python3
import argparse
import datetime
import time

from BigBlueButton import BigBlueButtonAutomation
from Jitsi import JitsiAutomation
from Webex import WebexAutomation
from Zoom import ZoomAutomation


def sleep_till_schedule(due_date):
    due_date = datetime.datetime(int(due_date[4:8]), int(due_date[2:4]), int(due_date[0:2]), int(due_date[8:10]),
                                 int(due_date[10:12]))
    while True:
        now = datetime.datetime.now()
        diff_date = due_date - now
        if diff_date.days == 0:
            # less than a day to sleep
            break
        else:
            # sleep for a day and try again
            time.sleep(24 * 60 * 60)
    # sleep remainder
    time.sleep(diff_date.seconds)


def config_meeting(args):
    if args.s:
        sleep_till_schedule(args.s)

    name = "" if args.n is None else args.n
    email = "" if args.e is None else args.e

    if "webex.com" in args.u:
        meeting = WebexAutomation(args.u, name, email, args.i)
    elif "zoom.us" in args.u:
        meeting = ZoomAutomation(args.u)
    elif "bbb.fslab.de" in args.u:
        meeting = BigBlueButtonAutomation(args.u, name)
    elif "meet." in args.u:
        meeting = JitsiAutomation(args.u, name)
    else:
        print("Meeting platform not supported")
        raise Exception

    meeting.start_meeting()

    if args.r:
        meeting.start_recording()

    meeting.wait_for_session_duration(args.d)
    meeting.end_meeting(args.o)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automatically enter and record meeting')
    parser.add_argument('-u', type=str, help='Url to meeting')
    parser.add_argument('-n', type=str, nargs="?", help='Name to display')
    parser.add_argument('-d', type=int, help='Meeting duration in minutes')
    parser.add_argument('-s', type=str, nargs="?", help='Schedule Time/Date DDMMYYYYHHMM')
    parser.add_argument('-e', type=str, nargs="?", help='Email to display')
    parser.add_argument('-r', action='store_true', help='Flag to start recording')
    parser.add_argument('-o', action='store_true', help='Flag if hotkeys are being used in OBS')
    parser.add_argument('-i', action='store_true', help='Set flag if link leads to meeting invite page')
    parser.add_argument('--dry', action='store_true',
                        help='Dry run: Webex test website will open so you can configure OBS. Default duration 2 minutes')

    args = parser.parse_args()

    if args.dry:
        meeting = WebexAutomation("https://www.webex.com/de/test-meeting.html")
        meeting.dry_run(args.d)
    else:
        config_meeting(args)
