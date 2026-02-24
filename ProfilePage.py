from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class ProfilePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def tap_send_feedback(self):
        send_feedback_btn = self.driver.find_element(By.ID, 'send-feedback-btn')
        send_feedback_btn.click()
