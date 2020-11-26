import os
import shutil
import signal
import subprocess
import time

from MeetingBase import MeetingAutomation


class ZoomAutomation(MeetingAutomation):
    def __init__(self, url):
        super().__init__(url)
        self.zoom_process = None

    def start_meeting(self):
        if shutil.which('zoom'):
            arg = '--url=zoommtg://' + self.url
            cmd = ["zoom", arg]
        elif shutil.which('zoom-client'):
            arg = '--url=' + self.url
            cmd = ["zoom-client", arg]
            print(cmd)
        else:
            print("No suitable Zoom client found!")
            print("Run 'snap install zoom' or 'sudo apt install zoom'")
            raise Exception
        self.zoom_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        time.sleep(25)

    def end_meeting(self, is_hotkeys_used):
        super().stop_recording(is_hotkeys_used)
        os.kill(self.zoom_process.pid, signal.SIGKILL)
        exit(0)
