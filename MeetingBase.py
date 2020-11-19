import os
import signal
import subprocess
import time

import pyautogui


class MeetingAutomation():

    def __init__(self, url):
        self.url = url
        self.driver = None
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

    def stop_recording(self, is_hotkeys_used):
        if not self.record_process:
            return
        if is_hotkeys_used:
            pyautogui.hotkey('ctrl', 'alt', 's') # TODO choose better key and argparse
            time.sleep(2)
        os.kill(self.record_process.pid, signal.SIGKILL)

    def end_meeting(self, is_hotkeys_used):
        self.stop_recording(is_hotkeys_used)
        self.driver.close()
