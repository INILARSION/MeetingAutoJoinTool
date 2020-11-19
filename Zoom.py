from MeetingBase import MeetingAutomation


class ZoomAutomation(MeetingAutomation):
    def __init__(self, url):
        super().__init__(url)

    def start_meeting(self):
        self._open_url()
