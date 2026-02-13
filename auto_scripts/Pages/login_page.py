from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    LOGIN_URL = "https://example.com/login"  # Example URL, replace with actual if available
    EMAIL_INPUT = (By.ID, "email_input")
    PASSWORD_INPUT = (By.ID, "password_input")
    LOGIN_BUTTON = (By.ID, "login_button")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@class='success']")
    USER_SESSION_INDICATOR = (By.ID, "user_session")
    INVALID_USERNAME_INPUT = (By.ID, "username_input_invalid")
    VALID_PASSWORD_INPUT = (By.ID, "password_input_valid")
    FAILURE_MESSAGE = (By.XPATH, "//div[@class='error']")
    LOGIN_PAGE_INDICATOR = (By.ID, "login_page_indicator")

    # Actions
    def navigate_to_login(self):
        self.driver.get(self.LOGIN_URL)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def enter_invalid_username(self, username):
        self.enter_text(self.INVALID_USERNAME_INPUT, username)

    def enter_valid_password(self, password):
        self.enter_text(self.VALID_PASSWORD_INPUT, password)

    # Validations
    def verify_login_success(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE)

    def verify_user_session(self):
        return self.is_element_visible(self.USER_SESSION_INDICATOR)

    def verify_login_failure(self):
        return self.is_element_visible(self.FAILURE_MESSAGE)

    def verify_remain_on_login(self):
        return self.is_element_visible(self.LOGIN_PAGE_INDICATOR)
