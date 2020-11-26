import os
import signal
import subprocess
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from meeting_base import MeetingAutomation


class WebexAutomation(MeetingAutomation):
    def __init__(self, url, name="test", email="test@test.com"):
        super().__init__(url)
        self.name = name
        self.email = email
        self.name_input = None
        self.email_input = None
        self.connect_button = None

    def start_meeting(self):
        self._set_driver()
        super()._open_url()
        self._join()
        self._login()

    def dry_run(self, duration):
        self._set_driver()
        super()._open_url()
        self.record_process = subprocess.Popen(["obs", "--multi"], stdout=subprocess.PIPE)
        self.wait_for_session_duration(duration if duration else 2)
        os.kill(self.record_process.pid, signal.SIGKILL)

    def _set_driver(self):
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

    def _set_credentials(self):
        if not (self.name_input is None or self.email_input is None):
            self.name_input.clear()
            self.name_input.send_keys(self.name)
            self.email_input.clear()
            self.email_input.send_keys(self.email)

    def _join(self):
        wait = WebDriverWait(self.driver, 10)

        try:
            self.driver.find_element_by_id("smartJoinButton").click()
            time.sleep(2)
        except NoSuchElementException:
            print('no invite / join room button, skipping')

        iframe_pbui = wait.until(expected_conditions.presence_of_element_located((By.ID, 'pbui_iframe')))
        if iframe_pbui:
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
        time.sleep(5)
        # if switched to iframe, switch back
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))

        # sometimes a field pops up, this closes it
        buttons = self.driver.find_elements_by_tag_name("button")
        btn_allow_names = ["Alles", "All"]
        for button in buttons:
            if any(x in button.get_attribute("innerHTML") for x in btn_allow_names):
                button.click()
                time.sleep(3)
                break

        # switch back from iframe
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))
        buttons = self.driver.find_elements_by_tag_name("button")
        # disable video and mic
        btn_stop_video = ["Video stoppen", "Stop"]
        btn_mute = ["Mute", "Stummschalten"]
        for button in buttons:
            if any(x in button.get_attribute("innerHTML") for x in (btn_mute + btn_stop_video)):
                button.click()
        # join meeting
        self.driver.find_element_by_id("interstitial_join_btn").click()
