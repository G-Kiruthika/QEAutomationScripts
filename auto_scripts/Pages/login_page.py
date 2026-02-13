from selenium.webdriver.common.by import By
from framework.base_page import BasePage  # Ensure this import matches your project structure

class LoginPage(BasePage):
    LOGIN_URL = "https://example.com/login"
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".validation-error")
    ACCOUNT_LOCKOUT_MESSAGE = (By.CSS_SELECTOR, ".account-lockout")
    EMAIL_NOTIFICATION = (By.CSS_SELECTOR, ".email-notification")

    def navigate_to_login_page(self):
        self.driver.get(self.LOGIN_URL)

    def enter_username(self, username):
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)

    def verify_validation_error(self):
        return self.is_displayed(self.VALIDATION_ERROR)

    def verify_login_prevented(self):
        return not self.is_enabled(self.LOGIN_BUTTON)

    def verify_account_lockout_message(self):
        return self.is_displayed(self.ACCOUNT_LOCKOUT_MESSAGE)

    def verify_email_notification_sent(self):
        return self.is_displayed(self.EMAIL_NOTIFICATION)