from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from meeting_base import MeetingAutomation


class JitsiAutomation(MeetingAutomation):
    def __init__(self, url, name):
        super().__init__(url)
        self.name = name

    def _set_name(self):
        input_field = self.driver.find_element_by_class_name("field")
        input_field.clear()
        input_field.send_keys(self.name)

    def _enter_meeting(self):
        self._set_name()
        self.driver.find_element_by_class_name("action-btn").click()

    def _set_driver(self):
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        })
        self.driver = webdriver.Chrome(options=opt)

    def start_meeting(self):
        self._set_driver()
        super()._open_url()
        self._enter_meeting()
