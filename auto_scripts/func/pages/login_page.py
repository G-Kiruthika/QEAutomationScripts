"""Login Page Object

This module contains the LoginPage class with all locators and methods
for interacting with the login page.
Follows Page Object Model (POM) pattern.
"""

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    """LoginPage class for login functionality
    
    Inherits from BasePage and provides login-specific methods.
    """
    
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    USER_PROFILE = (By.ID, "user-profile")
    LOGIN_FORM = (By.ID, "login-form")
    
    def navigate_to_login_page(self, url):
        """Navigate to the login page
        
        Args:
            url (str): The URL of the login page
        """
        self.driver.get(url)
    
    def validate_login_page_displayed(self):
        """Validate that the login page is displayed
        
        Returns:
            bool: True if login page is displayed, False otherwise
        """
        return self.is_element_visible(self.LOGIN_FORM)
    
    def enter_email(self, email):
        """Enter email in the email input field
        
        Args:
            email (str): Email address to enter
        """
        self.enter_text(self.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        """Enter password in the password input field
        
        Args:
            password (str): Password to enter
        """
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click the login button"""
        self.click_element(self.LOGIN_BUTTON)
    
    def validate_user_authenticated(self):
        """Validate that user is authenticated
        
        Returns:
            bool: True if user is authenticated, False otherwise
        """
        return self.is_element_visible(self.USER_PROFILE)
    
    def validate_error_message_displayed(self):
        """Validate that error message is displayed
        
        Returns:
            bool: True if error message is displayed, False otherwise
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def validate_user_not_authenticated(self):
        """Validate that user is not authenticated
        
        Returns:
            bool: True if user is not authenticated, False otherwise
        """
        return not self.is_element_visible(self.USER_PROFILE)
