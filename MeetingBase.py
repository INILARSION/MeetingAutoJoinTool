import os
import signal
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class MeetingAutomation():

    def __init__(self, url):
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
        self.record_process = None

    def _open_url(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    @staticmethod
    def wait_for_session_duration(minutes):
        time.sleep(minutes * 60)

    def start_recording(self):
        self.record_process = subprocess.Popen(["obs", "--startrecording", "--minimize-to-tray", "--multi"],
                                               stdout=subprocess.PIPE)

    def stop_recording(self):
        if self.record_process:
            os.kill(self.record_process.pid, signal.SIGKILL)

    def end_meeting(self):
        self.stop_recording()
        self.driver.close()
