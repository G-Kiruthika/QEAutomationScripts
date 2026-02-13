from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    EMAIL_INPUT = (By.ID, 'email_input')
    EMAIL_INPUT_XPATH = (By.XPATH, "//input[@name='email']")
    SUBMIT_BUTTON = (By.ID, 'submit_button')
    ERROR_MESSAGE = (By.ID, 'error_message')
    CONFIRMATION_MESSAGE = (By.ID, 'confirmation_message')
    FIRST_NAME_INPUT = (By.XPATH, "//input[@name='first_name']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@name='last_name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='password']")
    REGISTER_BUTTON = (By.XPATH, "//button[@id='register']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@class='success-message']")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_name(self, name):
        self.enter_text(self.NAME_FIELD, name)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_register(self):
        self.click_element(self.REGISTER_BUTTON)

    def submit_registration(self):
        self.click_element(self.SUBMIT_BUTTON)

    def is_confirmation_displayed(self):
        return self.is_element_visible(self.CONFIRMATION_MESSAGE)

    def is_error_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)

    def enter_first_name(self, first_name):
        self.enter_text(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        self.enter_text(self.LAST_NAME_INPUT, last_name)

    def click_register_button(self):
        self.click_element(self.REGISTER_BUTTON)

    def get_success_message(self):
        return self.get_element_text(self.SUCCESS_MESSAGE)

    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE)

    def validate_error_message(self, expected_message):
        return self.get_element_text(self.ERROR_MESSAGE) == expected_message

    def validate_registration_failed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)
