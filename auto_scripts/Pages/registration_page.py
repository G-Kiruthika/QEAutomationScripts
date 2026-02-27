from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.base_page import BasePage

class RegistrationPage(BasePage):
    # Locators
    email_input = (By.ID, "email_input_placeholder")
    password_input = (By.ID, "password_input_placeholder")
    name_input = (By.ID, "name_input_placeholder")
    register_button = (By.ID, "register_button_placeholder")
    error_message = (By.ID, "error_message_placeholder")

    def __init__(self, driver):
        super().__init__(driver)

    # Action Methods
    def enter_email(self, email):
        """Enter email in the email input field"""
        self.send_keys(self.email_input, email)

    def enter_password(self, password):
        """Enter password in the password input field"""
        self.send_keys(self.password_input, password)

    def enter_name(self, name):
        """Enter name in the name input field"""
        self.send_keys(self.name_input, name)

    def submit_registration(self):
        """Click the register button to submit registration"""
        self.click(self.register_button)

    # Validation Methods
    def validate_registration_page_displayed(self):
        """Validate that the registration page is displayed"""
        return self.is_element_visible(self.register_button)

    def validate_fields_accept_input(self):
        """Validate that all input fields accept input"""
        email_enabled = self.is_element_enabled(self.email_input)
        password_enabled = self.is_element_enabled(self.password_input)
        name_enabled = self.is_element_enabled(self.name_input)
        return email_enabled and password_enabled and name_enabled

    def validate_registration_success(self):
        """Validate successful registration"""
        # This would typically check for success indicators like redirect or success message
        return not self.is_element_visible(self.error_message)

    def validate_error_message(self, expected_error):
        """Validate that the expected error message is displayed"""
        if self.is_element_visible(self.error_message):
            actual_error = self.get_text(self.error_message)
            return expected_error in actual_error
        return False
