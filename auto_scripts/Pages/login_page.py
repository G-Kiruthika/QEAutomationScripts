from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    # Added from metadata
    ADMIN_LOGIN_LOCATOR = (By.ID, "placeholder_admin_login_locator")
    ADMIN_LOGIN_SUCCESS_LOCATOR = (By.ID, "placeholder_admin_login_success_locator")

    # New locators from metadata
    EMAIL_FIELD = (By.CSS_SELECTOR, "#email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#password")
    LOGIN_BUTTON_METADATA = (By.CSS_SELECTOR, "#loginBtn")
    DASHBOARD = (By.CSS_SELECTOR, "#dashboard")
    USER_HEADER = (By.CSS_SELECTOR, "#userHeader")
    LOGIN_ERROR_MSG = (By.CSS_SELECTOR, "#loginErrorMsg")
    LOGIN_PAGE = (By.CSS_SELECTOR, "#loginPage")

    def enter_username(self, username):
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def is_login_button_visible(self):
        return self.is_visible(self.LOGIN_BUTTON)

    # Added from metadata
    def login_as_admin(self, username, password):
        """Login as admin user using valid credentials."""
        self.send_keys(self.ADMIN_LOGIN_LOCATOR, username)
        self.send_keys(self.ADMIN_LOGIN_LOCATOR, password)
        self.click(self.LOGIN_BUTTON)

    def assert_admin_login_successful(self):
        """Verify admin login was successful."""
        return self.is_visible(self.ADMIN_LOGIN_SUCCESS_LOCATOR)

    # Action methods from metadata
    def navigate_to_login_page(self, url):
        self.driver.get(url)
        return self.is_element_visible(self.LOGIN_PAGE)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_FIELD, email)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_FIELD, password)

    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON_METADATA)

    def verify_user_session_created(self):
        return self.is_element_visible(self.DASHBOARD)

    # Validation methods from metadata
    def is_login_page_displayed(self):
        return self.is_element_visible(self.LOGIN_PAGE)

    def is_email_accepted(self):
        # Simple check: after entering email, field contains the value
        entered_email = self.get_element_value(self.EMAIL_FIELD)
        return bool(entered_email)

    def is_password_masked(self):
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        return password_field.get_attribute("type") == "password"

    def is_user_authenticated(self):
        return self.is_element_visible(self.USER_HEADER)

    def is_error_message_displayed(self):
        return self.is_element_visible(self.LOGIN_ERROR_MSG)

    def is_user_not_authenticated(self):
        return not self.is_element_visible(self.USER_HEADER)

    # Helper wrappers (if not already present in BasePage)
    def enter_text(self, locator, text):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def click_element(self, locator):
        element = self.driver.find_element(*locator)
        element.click()

    def is_element_visible(self, locator):
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except Exception:
            return False

    def get_element_value(self, locator):
        element = self.driver.find_element(*locator)
        return element.get_attribute("value")
