from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators from metadata (no duplicates, all required)
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'loginBtn')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.error-msg')
    VALIDATION_ERROR_MESSAGE = ('placeholder_locator_validation_error_message',)
    ACCOUNT_LOCKOUT_MESSAGE = ('placeholder_locator_account_lockout_message',)
    EMAIL_NOTIFICATION = ('placeholder_locator_email_notification',)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Actions from metadata
    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)

    def navigate_to_login_page(self, url):
        self.driver.get(url)

    def get_validation_error_message(self):
        if self.is_element_visible(self.VALIDATION_ERROR_MESSAGE):
            return self.get_element_text(self.VALIDATION_ERROR_MESSAGE)
        return None

    def get_account_lockout_message(self):
        if self.is_element_visible(self.ACCOUNT_LOCKOUT_MESSAGE):
            return self.get_element_text(self.ACCOUNT_LOCKOUT_MESSAGE)
        return None

    def verify_email_notification_sent(self):
        return self.is_element_visible(self.EMAIL_NOTIFICATION)

    # Validations from metadata
    def is_error_message_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)

    def get_error_message_text(self):
        return self.get_element_text(self.ERROR_MESSAGE)
