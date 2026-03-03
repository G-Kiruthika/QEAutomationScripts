from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import yaml

class RegistrationPage(BasePage):
    """Page object for user registration functionality"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirm_password")
    REGISTER_BUTTON = (By.ID, "register_button")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    REGISTRATION_FORM = (By.ID, "registration_form")
    
    def __init__(self, driver):
        super().__init__(driver)
        with open('config/config.yaml') as f:
            self.config = yaml.safe_load(f)
    
    def navigate_to_registration(self):
        """Navigate to registration page"""
        registration_url = f"{self.config['base_url']}/register"
        self.navigate_to(registration_url)
        self.wait_for_element(self.REGISTRATION_FORM)
    
    def fill_registration_form(self, username, email, password, confirm_password):
        """Fill out the registration form with provided data"""
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.enter_text(self.CONFIRM_PASSWORD_INPUT, confirm_password)
    
    def submit_registration(self):
        """Submit the registration form"""
        self.click_element(self.REGISTER_BUTTON)
    
    def get_success_message(self):
        """Get success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_registration_form_visible(self):
        """Check if registration form is visible"""
        return self.is_element_visible(self.REGISTRATION_FORM)
    
    def clear_form(self):
        """Clear all form fields"""
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.CONFIRM_PASSWORD_INPUT).clear()