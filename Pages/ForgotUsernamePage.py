# ForgotUsernamePage.py
'''
PageClass for Forgot Username Workflow
Handles username recovery instructions and retrieval.
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class ForgotUsernamePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.email_field = driver.find_element(By.ID, 'email')  # Example locator
        self.submit_button = driver.find_element(By.ID, 'submitBtn')  # Example locator
        self.confirmation_message = driver.find_element(By.ID, 'confirmationMsg')  # Example locator

    def recover_username(self, email):
        '''Follows instructions to recover username.'''
        self.email_field.send_keys(email)
        self.submit_button.click()

    def get_confirmation_message(self):
        '''Retrieves confirmation message after recovery.'''
        return self.confirmation_message.text
