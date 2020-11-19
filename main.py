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

    def open_url(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def goto_meeting(self):
        time.sleep(1)
        self.driver.find_element_by_id("smartJoinButton").click()

    def get_elements_login(self, set_credentials):
        try:
            time.sleep(2)
            self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))
        except:
            print("No nested iframe")

        if set_credentials:
            try:
                self.name_input = self.driver.find_element_by_id("full-name")
            except Exception as e:
                print(e)
            try:
                self.email_input = self.driver.find_element_by_id("email-address")
            except Exception as e:
                print(e)

            if self.name_input is None or self.email_input is None:
                inputs = self.driver.find_elements_by_tag_name("input")
                self.name_input = inputs[0]
                self.email_input = inputs[1]

            self._set_credentials()
        try:
            self.connect_button = self.driver.find_element_by_class_name('form_button')
        except Exception as e:
            print(e)
        if self.connect_button is None:
            try:
                self.connect_button = self.driver.find_element_by_class_name('tm-btn')
            except Exception as e:
                print(e)
        if self.connect_button is None:
            try:
                self.connect_button = self.driver.find_element_by_id('guest_next-btn')
            except Exception as e:
                print(e)

    @staticmethod
    def wait_for_session_duration(minutes):
        time.sleep(minutes * 60)

    def login(self):
        self.connect_button.click()
        time.sleep(1)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))
        buttons = self.driver.find_elements_by_tag_name("button")
        for button in buttons:
            if "Alles" in button.get_attribute("innerHTML"):
                button.click()
                break

        time.sleep(1)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))
        buttons = self.driver.find_elements_by_tag_name("button")
        for button in buttons:
            if "Video stoppen" in button.get_attribute("innerHTML") or "Stummschalten" in button.get_attribute(
                    "innerHTML"):
                button.click()
        self.driver.find_element_by_id("interstitial_join_btn").click()

    def close_window(self):
        if self.record_process:
            os.kill(self.record_process.pid, signal.SIGKILL)
        self.driver.close()

    def start_obs(self):
        self.record_process = subprocess.Popen(["obs", "--startrecording"], stdout=subprocess.PIPE)

    def _set_credentials(self):
        if not (self.name_input is None or self.email_input is None):
            self.name_input.clear()
            self.name_input.send_keys(self.name)
            self.email_input.clear()
            self.email_input.send_keys(self.email)


if __name__ == '__main__':
    #meeting = MeetingAutomation("https://www.webex.com/de/test-meeting.html", "test", "test@test.com")
    #meeting = MeetingAutomation("https://fu-berlin.webex.com/webappng/sites/fu-berlin/meeting/download/56b2fd2b045ea3a55517afc9c5efc4e3", "test", "test@test.com")
    meeting = MeetingAutomation("https://h-brs.webex.com/h-brs/j.php?MTID=m498e6a88dd7f97e8a9ebe2014ab89313", "Torsten", "")
    meeting.start_obs()
    meeting.open_url()
    meeting.goto_meeting()
    meeting.get_elements_login(True)
    meeting.login()
    meeting.wait_for_session_duration(0.5)
    meeting.close_window()
