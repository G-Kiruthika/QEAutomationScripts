from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    # Added from metadata
    ADMIN_LOGIN_LOCATOR = (By.ID, "placeholder_admin_login_locator")
    ADMIN_LOGIN_SUCCESS_LOCATOR = (By.ID, "placeholder_admin_login_success_locator")

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
