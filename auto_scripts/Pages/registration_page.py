from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
 EMAIL_INPUT = (By.ID, 'email_input')
 SUBMIT_BUTTON = (By.ID, 'submit_button')
 ERROR_MESSAGE = (By.ID, 'error_message')
 CONFIRMATION_MESSAGE = (By.ID, 'confirmation_message')

 def __init__(self, driver):
 super().__init__(driver)

 def enter_email(self, email):
 self.enter_text(self.EMAIL_INPUT, email)

 def submit_registration(self):
 self.click_element(self.SUBMIT_BUTTON)

 def is_confirmation_displayed(self):
 return self.is_element_visible(self.CONFIRMATION_MESSAGE)

 def is_error_displayed(self):
 return self.is_element_visible(self.ERROR_MESSAGE)
