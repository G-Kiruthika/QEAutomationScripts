# auto_scripts/Pages/registration_page.py

from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class RegistrationPage(BasePage):
    # Existing locators and methods preserved
    # Locators
    USERNAME_INPUT = (By.ID, "usernameInput")
    PASSWORD_INPUT = (By.ID, "passwordInput")
    SUBMIT_BUTTON = (By.XPATH, "//button[@id='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")

    # Actions
    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    # Validations
    def is_success_message_visible(self):
        return self.is_visible(self.SUCCESS_MESSAGE)
