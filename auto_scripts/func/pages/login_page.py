from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')
    VALIDATION_ERROR = (By.ID, 'validation-error')
    ERROR_MESSAGE = (By.CLASS_NAME, 'error-message')
    ACCOUNT_LOCKED_MESSAGE = (By.ID, 'account-locked-message')

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_login(self, url):
        self.driver.get(url)

    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)

    def get_validation_error(self):
        return self.get_element_text(self.VALIDATION_ERROR)

    def is_validation_error_displayed(self):
        return self.is_element_visible(self.VALIDATION_ERROR)

    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE)

    def is_error_message_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)

    def verify_account_lockout_notification(self):
        return self.is_element_visible(self.ACCOUNT_LOCKED_MESSAGE)

    def get_account_locked_message(self):
        return self.get_element_text(self.ACCOUNT_LOCKED_MESSAGE)
