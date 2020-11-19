import argparse
import datetime
import os
import signal
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class MeetingAutomation:
    def __init__(self, url, name="test", email="test@test.com"):
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1
        })
        self.driver = webdriver.Chrome(options=opt)
        self.url = url
        self.name = name
        self.email = email
        self.name_input = None
        self.email_input = None
        self.connect_button = None
        self.record_process = None

    def _open_url(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def _goto_meeting(self):
        # wait for page to load fully
        time.sleep(1)
        self.driver.find_element_by_id("smartJoinButton").click()

    def _get_elements_login(self):
        # sometimes there is an iframe, sometimes not
        if self.driver.find_elements_by_id("pbui_iframe"):
            # wait for page to load fully
            time.sleep(1)
            self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))

        if self.driver.find_elements_by_id("full-name"):
            self.name_input = self.driver.find_element_by_id("full-name")
        elif self.driver.find_elements_by_id("email-address"):
            self.email_input = self.driver.find_element_by_id("email-address")
        else:
            inputs = self.driver.find_elements_by_tag_name("input")
            self.name_input = inputs[0]
            self.email_input = inputs[1]
        self._set_credentials()

        if self.driver.find_elements_by_class_name('form_button'):
            self.connect_button = self.driver.find_element_by_class_name('form_button')
        elif self.driver.find_elements_by_class_name('tm-btn'):
            self.connect_button = self.driver.find_element_by_class_name('tm-btn')
        else:
            self.connect_button = self.driver.find_element_by_id('guest_next-btn')

    @staticmethod
    def wait_for_session_duration(minutes):
        time.sleep(minutes * 60)

    def _login(self):
        self.connect_button.click()
        # wait for page to load fully
        time.sleep(1)
        # if switched to iframe, switch back
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))

        # sometimes a field pops up, this closes it
        buttons = self.driver.find_elements_by_tag_name("button")
        for button in buttons:
            if "Alles" in button.get_attribute("innerHTML"):
                button.click()
                break

        # wait for load again
        time.sleep(1)
        # switch back from iframe
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))
        buttons = self.driver.find_elements_by_tag_name("button")
        # disable video and mic
        for button in buttons:
            if "Video stoppen" in button.get_attribute("innerHTML") or "Stummschalten" in button.get_attribute(
                    "innerHTML"):
                button.click()
        # join meeting
        self.driver.find_element_by_id("interstitial_join_btn").click()

    def end_meeting(self):
        if self.record_process:
            os.kill(self.record_process.pid, signal.SIGKILL)
        self.driver.close()

    def start_recording(self):
        self.record_process = subprocess.Popen(["obs", "--startrecording", "--minimize-to-tray"], stdout=subprocess.PIPE)

    def _set_credentials(self):
        if not (self.name_input is None or self.email_input is None):
            self.name_input.clear()
            self.name_input.send_keys(self.name)
            self.email_input.clear()
            self.email_input.send_keys(self.email)

    def start_meeting(self, is_meeting_invite):
        self._open_url()
        if is_meeting_invite:
            self._goto_meeting()
        self._get_elements_login()
        self._login()


def sleep_till_schedule(due_date):
    due_date = datetime.datetime(int(due_date[4:8]), int(due_date[2:4]), int(due_date[0:2]))
    while True:
        now = datetime.datetime.now()
        diff_date = due_date - now
        if diff_date.hours == 0:
            # less than a day to sleep
            break
        else:
            # sleep for a day and try again
            time.sleep(24 * 60 * 60)
    # sleep remainder
    time.sleep(diff_date.seconds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automatically enter and record meeting')
    parser.add_argument('-u', type=str, help='Url to meeting')
    parser.add_argument('-n', type=str, help='Name to display')
    parser.add_argument('-d', type=int, help='Meeting duration in minutes')
    parser.add_argument('-s', type=str, nargs="?", help='Schedule Time/Date DDMMYYYYHHMM')
    parser.add_argument('-e', type=str, nargs="?", help='Email to display')
    parser.add_argument('-r', action='store_true', help='Flag to start recording')
    parser.add_argument('-i', action='store_true', help='Set flag if link leads to meeting invite page')

    args = parser.parse_args()

    if args.s:
        sleep_till_schedule(args.s)

    email = "" if args.e is None else args.e
    meeting = MeetingAutomation(args.u, args.n, email)

    meeting.start_meeting(args.i)

    if args.r:
        meeting.start_recording()

    meeting.wait_for_session_duration(args.d)
    meeting.end_meeting()
