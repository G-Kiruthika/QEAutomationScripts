import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    """Page Object for Login functionality of example-ecommerce.com"""

    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        """Initializes LoginPage with WebDriver instance."""
        self.driver = driver

    def navigate(self):
        """Navigates to the login page."""
        self.driver.get(self.URL)

    def enter_email(self, email: str):
        """Enters email into the email field."""
        email_elem = self.driver.find_element(*self.EMAIL_FIELD)
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password: str):
        """Enters password into the password field."""
        password_elem = self.driver.find_element(*self.PASSWORD_FIELD)
        password_elem.clear()
        password_elem.send_keys(password)

    def toggle_remember_me(self, enable: bool):
        """Sets the 'Remember Me' checkbox to the specified state."""
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if checkbox.is_selected() != enable:
            checkbox.click()

    def click_login(self):
        """Clicks the login submit button."""
        self.driver.find_element(*self.LOGIN_SUBMIT).click()

    def click_forgot_password(self):
        """Clicks the forgot password link."""
        self.driver.find_element(*self.FORGOT_PASSWORD_LINK).click()

    def get_error_message(self) -> str:
        """Returns the error message displayed after failed login."""
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def get_validation_error(self) -> str:
        """Returns validation error message for invalid input."""
        return self.driver.find_element(*self.VALIDATION_ERROR).text

    def is_empty_field_prompt_displayed(self) -> bool:
        """Checks if the mandatory fields prompt is displayed."""
        try:
            elem = self.driver.find_element(*self.EMPTY_FIELD_PROMPT)
            return elem.is_displayed()
        except Exception:
            return False

    def is_dashboard_header_displayed(self) -> bool:
        """Checks if dashboard header is visible after login."""
        try:
            elem = self.driver.find_element(*self.DASHBOARD_HEADER)
            return elem.is_displayed()
        except Exception:
            return False

    def is_user_profile_icon_displayed(self) -> bool:
        """Checks if user profile icon is visible after login."""
        try:
            elem = self.driver.find_element(*self.USER_PROFILE_ICON)
            return elem.is_displayed()
        except Exception:
            return False

    def login(self, email: str, password: str, remember_me: bool = False):
        """Performs login with given credentials and optional 'Remember Me'."""
        self.enter_email(email)
        self.enter_password(password)
        self.toggle_remember_me(remember_me)
        self.click_login()
        time.sleep(1)  # Wait for page load; replace with explicit waits for production

    def login_with_empty_fields(self):
        """Attempts login with empty fields for negative testing."""
        self.enter_email("")
        self.enter_password("")
        self.click_login()
        time.sleep(1)

    def verify_remember_me_functionality(self) -> bool:
        """Verifies 'Remember Me' persists login after browser restart."""
        # This method should be implemented in test scripts using session/cookie management.
        # Placeholder for downstream automation agent.
        pass
