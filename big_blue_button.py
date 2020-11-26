import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from meeting_base import MeetingAutomation


class BigBlueButtonAutomation(MeetingAutomation):
    def __init__(self, url, name):
        super().__init__(url)
        self.name = name

    def _set_name_consent(self):
        for input_element in self.driver.find_elements_by_tag_name("input"):
            if "join_name" in input_element.get_attribute("id"):
                try:
                    input_element.clear()
                    input_element.send_keys(self.name)
                except:
                    pass
                break
        consent_check = self.driver.find_elements_by_id("joiner-consent")
        if consent_check:
            consent_check[0].click()

    def _set_sound(self):
        # click audio button
        for button in self.driver.find_elements_by_tag_name("button"):
            if "Mikrofon" in button.get_attribute("innerHTML"):
                button.click()
                break
        # wait for echo test
        time.sleep(10)
        # click yes on echo test
        for button in self.driver.find_elements_by_tag_name("button"):
            if "Ja" in button.get_attribute("innerHTML"):
                button.click()
                break
        # let room load again
        time.sleep(3)
        # mute yourself
        for button in self.driver.find_elements_by_tag_name("button"):
            if "Stummschalten" in button.get_attribute("innerHTML"):
                button.click()
                break

    def _enter_meeting(self):
        self._set_name_consent()
        self.driver.find_element_by_id("room-join").click()
        # wait for room to load
        time.sleep(10)
        self._set_sound()

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

    def start_meeting(self):
        self._set_driver()
        super()._open_url()
        self._enter_meeting()
