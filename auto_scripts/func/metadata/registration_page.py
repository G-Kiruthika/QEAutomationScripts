from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    """Page Object Model for Registration Page"""
    
    # URL
    REGISTRATION_URL = "registration_url"
    
    # Locators
    FIRST_NAME_INPUT = (By.ID, "first_name_input")
    LAST_NAME_INPUT = (By.ID, "last_name_input")
    EMAIL_INPUT = (By.ID, "email_input")
    PASSWORD_INPUT = (By.ID, "password_input")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirm_password_input")
    REGISTER_BUTTON = (By.ID, "register_button")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "success_message")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "error_message")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_registration(self):
        """Navigate to the registration page"""
        self.driver.get(self.REGISTRATION_URL)
    
    def enter_first_name(self, first_name):
        """Enter first name in the first name input field"""
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name in the last name input field"""
        self.enter_text(self.LAST_NAME_INPUT, last_name)
    
    def enter_email(self, email):
        """Enter email in the email input field"""
        self.enter_text(self.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        """Enter password in the password input field"""
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def enter_confirm_password(self, confirm_password):
        """Enter confirm password in the confirm password input field"""
        self.enter_text(self.CONFIRM_PASSWORD_INPUT, confirm_password)
    
    def click_register_button(self):
        """Click the register button"""
        self.click_element(self.REGISTER_BUTTON)
    
    def get_success_message(self):
        """Get the success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def get_error_message(self):
        """Get the error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_success_message_visible(self):
        """Check if success message is visible"""
        return self.is_element_visible(self.SUCCESS_MESSAGE)
    
    def is_error_message_visible(self):
        """Check if error message is visible"""
        return self.is_element_visible(self.ERROR_MESSAGE)