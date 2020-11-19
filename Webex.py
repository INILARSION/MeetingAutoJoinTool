import os
import signal
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebexAutomation:
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

    def _set_credentials(self):
        if not (self.name_input is None or self.email_input is None):
            self.name_input.clear()
            self.name_input.send_keys(self.name)
            self.email_input.clear()
            self.email_input.send_keys(self.email)

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

    def dry_run(self, duration):
        self._open_url()
        self.record_process = subprocess.Popen(["obs", "--multi"], stdout=subprocess.PIPE)
        self.wait_for_session_duration(duration if duration else 2)
        os.kill(self.record_process.pid, signal.SIGKILL)

    def start_meeting(self, is_meeting_invite):
        self._open_url()
        if is_meeting_invite:
            self._goto_meeting()
        self._get_elements_login()
        self._login()

    def end_meeting(self):
        if self.record_process:
            os.kill(self.record_process.pid, signal.SIGKILL)
        self.driver.close()

    def start_recording(self):
        self.record_process = subprocess.Popen(["obs", "--startrecording", "--minimize-to-tray", "--multi"],
                                               stdout=subprocess.PIPE)

    @staticmethod
    def wait_for_session_duration(minutes):
        time.sleep(minutes * 60)




