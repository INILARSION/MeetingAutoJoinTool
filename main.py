import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class MeetingAutomation:
    def __init__(self, url, name, email):
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.set_preference("permissions.default.microphone", 1)
        opt.set_preference("permissions.default.camera", 1)
        self.driver = webdriver.Firefox(options=opt)
        self.url = url
        self.name = name
        self.email = email
        self.name_input = None
        self.email_input = None
        self.connect_button = None

    def open_url(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def get_elements_first_page(self):
        try:
            time.sleep(3)
            self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))
        except:
            print("No nested iframe")
        try:
            self.name_input = self.driver.find_element_by_id("full-name")
        except Exception as e:
            print(e)
        try:
            self.email_input = self.driver.find_element_by_id("email-address")
        except Exception as e:
            print(e)

        if self.name_input is None or self.email_input is None:
            inputs = self.driver.find_elements_by_tag_name("input")
            self.name_input = inputs[0]
            self.email_input = inputs[1]

        self.set_name()
        try:
            self.connect_button = self.driver.find_element_by_class_name('form_button')
        except Exception as e:
            print(e)
        if self.connect_button is None:
            try:
                self.connect_button = self.driver.find_element_by_class_name('tm-btn')
            except Exception as e:
                print(e)
        if self.connect_button is None:
            try:
                self.connect_button = self.driver.find_element_by_id('guest_next-btn')
            except Exception as e:
                print(e)

    @staticmethod
    def wait(minutes):
        time.sleep(minutes * 60)

    def login(self):
        self.connect_button.click()
        self.join_meeting()

    def join_meeting(self):
        time.sleep(20)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_id("pbui_iframe"))
        self.driver.find_element_by_id("interstitial_join_btn").click()

    def close_window(self):
        self.driver.close()

    def set_name(self):
        if not (self.name_input is None or self.email_input is None):
            self.name_input.clear()
            self.name_input.send_keys(self.name)
            self.email_input.clear()
            self.email_input.send_keys(self.email)


if __name__ == '__main__':
    #meeting = MeetingAutomation("https://www.webex.com/de/test-meeting.html")
    meeting = MeetingAutomation("https://fu-berlin.webex.com/webappng/sites/fu-berlin/meeting/download/56b2fd2b045ea3a55517afc9c5efc4e3", "test", "test@test.com")
    meeting.open_url()
    meeting.get_elements_first_page()
    meeting.login()
    meeting.wait(1)
    meeting.close_window()
