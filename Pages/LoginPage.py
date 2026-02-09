# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    """
    Page Object for Login Page.
    Implements actions and verifications for login scenarios.
    """
    # Locators (Assumed from context)
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'loginBtn')
    ERROR_MESSAGE = (By.ID, 'errorMsg')

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate_to_login_page(self, url: str):
        """Navigate to the login page."""
        self.driver.get(url)

    def enter_email(self, email: str):
        """Enter email into the email field."""
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)

    def leave_email_empty(self):
        """Ensure the email field is empty."""
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()

    def enter_password(self, password: str):
        """Enter password into the password field."""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)

    def click_login_button(self):
        """Click the login button."""
        login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
        login_btn.click()

    def is_login_page_displayed(self) -> bool:
        """Verify if login page is displayed."""
        return self.driver.find_element(*self.EMAIL_INPUT).is_displayed() and \
               self.driver.find_element(*self.PASSWORD_INPUT).is_displayed()

    def is_email_field_empty(self) -> bool:
        """Check if the email field is empty."""
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        return email_field.get_attribute('value') == ''

    def is_password_accepted(self, expected_password: str) -> bool:
        """Verify if password is accepted (entered correctly)."""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        return password_field.get_attribute('value') == expected_password

    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed."""
        try:
            error_msg = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_msg.is_displayed()
        except Exception:
            return False

    def get_error_message_text(self) -> str:
        """Get the error message text."""
        error_msg = self.driver.find_element(*self.ERROR_MESSAGE)
        return error_msg.text

    def is_user_logged_in(self) -> bool:
        """Check if user is successfully logged in (e.g., redirected to dashboard)."""
        # Placeholder: implement based on application, e.g., check for dashboard element
        return 'dashboard' in self.driver.current_url or 'home' in self.driver.current_url
