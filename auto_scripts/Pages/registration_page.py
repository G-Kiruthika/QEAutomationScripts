from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class RegistrationPage(BasePage):
    REGISTRATION_URL = "<placeholder>"
    FIRST_NAME_INPUT = (By.ID, "<placeholder>")
    LAST_NAME_INPUT = (By.ID, "<placeholder>")
    EMAIL_INPUT = (By.ID, "<placeholder>")
    PASSWORD_INPUT = (By.ID, "<placeholder>")
    CONFIRM_PASSWORD_INPUT = (By.ID, "<placeholder>")
    REGISTER_BUTTON = (By.ID, "<placeholder>")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "<placeholder>")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "<placeholder>")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_registration(self):
        self.driver.get(self.REGISTRATION_URL)

    def enter_first_name(self, first_name):
        self.enter_text(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        self.enter_text(self.LAST_NAME_INPUT, last_name)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, confirm_password):
        self.enter_text(self.CONFIRM_PASSWORD_INPUT, confirm_password)

    def click_register_button(self):
        self.click_element(self.REGISTER_BUTTON)

    def get_success_message(self):
        return self.get_element_text(self.SUCCESS_MESSAGE)

    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE)

    def is_success_message_visible(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE)

    def is_error_message_visible(self):
        return self.is_element_visible(self.ERROR_MESSAGE)
