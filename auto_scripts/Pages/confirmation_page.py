from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ConfirmationPage(BasePage):
 CONFIRMATION_TEXT = (By.ID, 'confirmation_text')

 def __init__(self, driver):
 super().__init__(driver)

 def get_confirmation_text(self):
 return self.get_element_text(self.CONFIRMATION_TEXT)

 def is_confirmation_text_correct(self):
 return self.is_element_visible(self.CONFIRMATION_TEXT)
