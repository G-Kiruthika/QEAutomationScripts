from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object Model for Login Page"""

    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login_button")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    LOGIN_FORM = (By.ID, "login_form")
    LOCKOUT_NOTIFICATION = (By.CLASS_NAME, "lockout-notification")

    def __init__(self, driver):
        """Initialize LoginPage with driver"""
        super().__init__(driver)

    def is_login_page_displayed(self):
        """Check if login page is displayed"""
        return self.is_element_visible(self.LOGIN_FORM)

    def enter_username(self, username):
        """Enter username in the username field"""
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter password in the password field"""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Click the login button"""
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Get the error message text"""
        return self.get_element_text(self.ERROR_MESSAGE)

    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)

    def is_username_blank(self):
        """Check if username field is blank"""
        username_value = self.get_element_attribute(self.USERNAME_INPUT, "value")
        return username_value == ""

    def is_password_entered(self):
        """Check if password is entered"""
        password_value = self.get_element_attribute(self.PASSWORD_INPUT, "value")
        return password_value != ""

    def is_field_filled(self, field_name):
        """Check if a specific field is filled"""
        if field_name == "username":
            return self.get_element_attribute(self.USERNAME_INPUT, "value") != ""
        elif field_name == "password":
            return self.get_element_attribute(self.PASSWORD_INPUT, "value") != ""
        return False

    def is_account_lockout_notification_displayed(self):
        """Check if account lockout notification is displayed"""
        return self.is_element_visible(self.LOCKOUT_NOTIFICATION)
