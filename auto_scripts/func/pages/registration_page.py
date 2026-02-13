from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    """Page Object for User Registration functionality"""
    
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    NAME_INPUT = (By.ID, "name")
    REGISTER_BUTTON = (By.ID, "register-button")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def register_user(self, email, password=None, name=None):
        """Register a new user with provided details"""
        self.enter_text(self.EMAIL_INPUT, email)
        if password:
            self.enter_text(self.PASSWORD_INPUT, password)
        if name:
            self.enter_text(self.NAME_INPUT, name)
        self.click_element(self.REGISTER_BUTTON)
    
    def validate_registration_success(self):
        """Validate that registration was successful"""
        return self.is_element_visible(self.SUCCESS_MESSAGE)
    
    def validate_error_message(self):
        """Validate that error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)
