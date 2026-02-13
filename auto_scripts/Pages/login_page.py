# Existing imports and code should remain unchanged

class LoginPage(BasePage):
    # Existing locators
    USERNAME_INPUT = "//input[@id='username']"
    PASSWORD_INPUT = "//input[@id='password']"
    LOGIN_BUTTON = "//button[@id='login']"
    VALIDATION_ERROR = "//div[@class='validation-error']"
    ACCOUNT_LOCKOUT_MESSAGE = "//div[@class='lockout-message']"
    EMAIL_NOTIFICATION = "//div[@class='email-notification']"

    # Existing methods
    def navigate_to_login_page(self):
        self.driver.get("https://example.com/login")

    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)

    def verify_validation_error(self):
        return self.is_element_visible(self.VALIDATION_ERROR)

    def verify_login_prevented(self):
        # Typically checks if login button is disabled or user remains on login page
        return not self.driver.current_url.endswith("/dashboard")

    def verify_account_lockout_message(self):
        return self.is_element_visible(self.ACCOUNT_LOCKOUT_MESSAGE)

    def verify_email_notification_sent(self):
        return self.is_element_visible(self.EMAIL_NOTIFICATION)
