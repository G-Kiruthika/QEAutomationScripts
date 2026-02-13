from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    USER_NAME_HEADER = (By.ID, "userHeader")
    SESSION_TOKEN = (By.CSS_SELECTOR, '[data-attr="session-token"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")

    def navigate_to_login_page(self, url):
        self.driver.get(url)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_FIELD, email)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_FIELD, password)

    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)

    def is_login_page_displayed(self):
        return self.is_element_visible(self.EMAIL_FIELD) and self.is_element_visible(self.PASSWORD_FIELD) and self.is_element_visible(self.LOGIN_BUTTON)

    def is_email_accepted(self):
        return self.is_element_visible(self.EMAIL_FIELD)

    def is_password_accepted(self):
        return self.is_element_visible(self.PASSWORD_FIELD)

    def is_user_authenticated(self):
        return self.is_element_visible(self.USER_NAME_HEADER)

    def is_user_name_displayed(self):
        return self.is_element_visible(self.USER_NAME_HEADER)

    def is_session_token_generated(self):
        return self.is_element_visible(self.SESSION_TOKEN)

    def is_error_message_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)

    def is_on_login_page(self):
        return self.is_element_visible(self.EMAIL_FIELD) and self.is_element_visible(self.PASSWORD_FIELD)
