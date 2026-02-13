from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    # Added from metadata
    ADMIN_LOGIN_LOCATOR = (By.ID, "placeholder_admin_login_locator")
    ADMIN_LOGIN_SUCCESS_LOCATOR = (By.ID, "placeholder_admin_login_success_locator")
    # Appended locators from metadata
    USERNAME_FIELD = (By.ID, "placeholder_locator_username")
    PASSWORD_FIELD = (By.ID, "placeholder_locator_password")
    LOGIN_BUTTON_META = (By.ID, "placeholder_locator_login_button")
    VALIDATION_ERROR = (By.ID, "placeholder_locator_validation_error")

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

    # Appended actions from metadata
    def navigate_to_login_page(self):
        """Navigate to the login page."""
        self.go_to("/login")

    def enter_username_meta(self, username):
        """Enter username in the username field (metadata locator)."""
        self.send_keys(self.USERNAME_FIELD, username)

    def enter_password_meta(self, password):
        """Enter password in the password field (metadata locator)."""
        self.send_keys(self.PASSWORD_FIELD, password)

    def click_login_button_meta(self):
        """Click the Login button (metadata locator)."""
        self.click(self.LOGIN_BUTTON_META)

    # Appended validations from metadata
    def is_login_page_displayed(self):
        """Verify the login page is displayed."""
        return self.is_visible(self.LOGIN_BUTTON_META)

    def is_username_field_blank(self):
        """Verify the username field is blank."""
        return self.get_element_value(self.USERNAME_FIELD) == ""

    def is_validation_error_displayed(self):
        """Verify validation error is displayed."""
        return self.is_visible(self.VALIDATION_ERROR)

    def is_login_prevented(self):
        """Verify login is prevented and user remains on login page."""
        return self.is_visible(self.LOGIN_BUTTON_META)

    def is_account_locked_error_displayed(self):
        """Verify account locked error message is displayed."""
        return self.is_visible(self.VALIDATION_ERROR)

    def is_lockout_notification_sent(self):
        """Verify email notification is sent to user about account lockout."""
        # Placeholder for actual implementation
        return self.check_email_notification("account lockout")
