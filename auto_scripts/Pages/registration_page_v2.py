from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    EMAIL_INPUT = (By.ID, "email_input_placeholder")
    PASSWORD_INPUT = (By.ID, "password_input_placeholder")
    NAME_INPUT = (By.ID, "name_input_placeholder")
    REGISTER_BUTTON = (By.ID, "register_button_placeholder")
    ERROR_MESSAGE = (By.ID, "error_message_placeholder")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def enter_name(self, name):
        self.enter_text(self.NAME_INPUT, name)

    def submit_registration(self):
        self.click_element(self.REGISTER_BUTTON)

    def validate_registration_page_displayed(self):
        return self.is_element_visible(self.REGISTER_BUTTON)

    def validate_fields_accept_input(self):
        try:
            self.enter_text(self.EMAIL_INPUT, "test@example.com")
            self.enter_text(self.PASSWORD_INPUT, "password123")
            self.enter_text(self.NAME_INPUT, "Test User")
            return True
        except Exception:
            return False

    def validate_registration_success(self):
        # Implement actual logic for registration success validation
        return self.is_element_visible(self.REGISTER_BUTTON)  # Placeholder

    def validate_error_message(self, expected_error=None):
        if expected_error:
            return self.get_element_text(self.ERROR_MESSAGE) == expected_error
        return self.is_element_visible(self.ERROR_MESSAGE)
