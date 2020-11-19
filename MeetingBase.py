import os
import signal
import subprocess
import time


class MeetingAutomation():

    def __init__(self):
        self.record_process = None

    @staticmethod
    def wait_for_session_duration(minutes):
        time.sleep(minutes * 60)

    def start_recording(self):
        self.record_process = subprocess.Popen(["obs", "--startrecording", "--minimize-to-tray", "--multi"],
                                               stdout=subprocess.PIPE)

    def stop_recording(self):
        if self.record_process:
            os.kill(self.record_process.pid, signal.SIGKILL)
