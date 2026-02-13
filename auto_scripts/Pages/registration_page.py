from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class RegistrationPage(BasePage):
    EMAIL_INPUT = (By.ID, "email_input")
    SUBMIT_BUTTON = (By.ID, "submit_button")
    ERROR_MESSAGE = (By.ID, "error_message")
    CONFIRMATION_MESSAGE = (By.ID, "confirmation_message")

    # Newly appended locators
    FIRST_NAME_INPUT = (By.ID, "first_name_input")
    LAST_NAME_INPUT = (By.ID, "last_name_input")
    PASSWORD_INPUT = (By.ID, "password_input")
    REGISTER_BUTTON = (By.ID, "register_button")
    SUCCESS_MESSAGE = (By.ID, "success_message")
    
    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def submit_registration(self):
        self.click(self.SUBMIT_BUTTON)

    def is_confirmation_displayed(self):
        return self.is_visible(self.CONFIRMATION_MESSAGE)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_MESSAGE)

    # Newly appended methods
    def enter_first_name(self, first_name):
        self.enter_text(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        self.enter_text(self.LAST_NAME_INPUT, last_name)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_register_button(self):
        self.click(self.REGISTER_BUTTON)

    def get_success_message(self):
        if self.is_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return None

    def get_error_message(self):
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
