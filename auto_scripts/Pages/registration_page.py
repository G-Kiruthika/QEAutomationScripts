from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    # Locators from metadata - converted to UPPER_CASE with By constants
    EMAIL_INPUT = (By.ID, "email_input_placeholder")
    PASSWORD_INPUT = (By.ID, "password_input_placeholder")
    NAME_INPUT = (By.ID, "name_input_placeholder")
    REGISTER_BUTTON = (By.ID, "register_button_placeholder")
    ERROR_MESSAGE = (By.ID, "error_message_placeholder")

    def __init__(self, driver):
        super().__init__(driver)

    # Action methods from metadata using BasePage wrapper methods
    def enter_email(self, email):
        """Enter email address in the email input field."""
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        """Enter password in the password input field."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def enter_name(self, name):
        """Enter name in the name input field."""
        self.enter_text(self.NAME_INPUT, name)

    def submit_registration(self):
        """Click the registration submit button."""
        self.click_element(self.REGISTER_BUTTON)

    # Validation methods from metadata that return boolean and use visibility checks
    def validate_registration_page_displayed(self):
        """Validate that the registration page is displayed."""
        return self.is_element_visible(self.REGISTER_BUTTON)

    def validate_fields_accept_input(self):
        """Validate that all input fields accept input."""
        try:
            # Test input acceptance without actually submitting
            self.enter_text(self.EMAIL_INPUT, "test@example.com")
            self.enter_text(self.PASSWORD_INPUT, "password123")
            self.enter_text(self.NAME_INPUT, "Test User")
            return True
        except Exception:
            return False

    def validate_registration_success(self):
        """Validate that registration was successful."""
        # This should be implemented based on actual success indicators
        # For now, checking if we're redirected away from registration page
        try:
            return not self.is_element_visible(self.REGISTER_BUTTON)
        except Exception:
            return False

    def validate_error_message(self, expected_error=None):
        """Validate error message display and content."""
        if expected_error:
            return self.get_element_text(self.ERROR_MESSAGE) == expected_error
        return self.is_element_visible(self.ERROR_MESSAGE)