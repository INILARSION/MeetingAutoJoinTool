import os
import shutil
import signal
import subprocess
import sys
import time

from Xlib import display

from meeting_base import MeetingAutomation


class ZoomAutomation(MeetingAutomation):
    def __init__(self, url):
        super().__init__(url)
        self.zoom_process = None

    def start_meeting(self):
        self._start_zoom_process(self.url)
        time.sleep(25)

        while not self._is_meeting_window_open():
            os.kill(self.zoom_process.pid, signal.SIGKILL)
            time.sleep(5)
            self._start_zoom_process(self.url)
            time.sleep(60)

    def _start_zoom_process(self, url: str):
        if shutil.which('zoom'):
            arg = '--url=zoommtg://' + url
            cmd = ["zoom", arg]
        elif shutil.which('zoom-client'):
            arg = '--url=' + url
            cmd = ["zoom-client", arg]
            print(cmd)
        else:
            print("No suitable Zoom client found!")
            print("Run 'snap install zoom' or 'sudo apt install zoom'")
            raise Exception
        self.zoom_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    @staticmethod
    def _is_meeting_window_open() -> bool:
        """ Zoom opens window "zoom - free account" (on ubuntu, gnome-shell) """
        list_windows = display.Display().screen().root.query_tree()
        window_names = [x.get_wm_name().lower() for x in list_windows.children]

        return 'zoom -' in window_names

    def end_meeting(self, is_hotkeys_used):
        super().stop_recording(is_hotkeys_used)
        os.kill(self.zoom_process.pid, signal.SIGKILL)
        sys.exit(0)
