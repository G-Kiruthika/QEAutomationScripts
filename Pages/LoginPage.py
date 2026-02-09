# Pages/LoginPage.py
"""
Page Object Model for the Login Page of Example E-Commerce.
This class provides methods to interact with login form fields, submit actions, and validate login outcomes.

Test Cases Supported:
- TC_LOGIN_001: Valid login flow
- TC_LOGIN_002: Invalid login flow with error validation

Locators sourced from Locators.json.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"

    # Locators
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

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        """Navigate to the login page."""
        self.driver.get(self.URL)

    def enter_email(self, email):
        """Enter email in the email field."""
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        """Enter password in the password field."""
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def set_remember_me(self, value=True):
        """Set the 'Remember Me' checkbox."""
        checkbox = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX))
        if checkbox.is_selected() != value:
            checkbox.click()

    def click_login(self):
        """Click the login button."""
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()

    def click_forgot_password(self):
        """Click the 'Forgot Password' link."""
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        link.click()

    def get_error_message(self):
        """Get the error message displayed for invalid credentials."""
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text
        except:
            return None

    def get_validation_error(self):
        """Get validation error message for empty or invalid fields."""
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return error.text
        except:
            return None

    def is_empty_field_prompt_displayed(self):
        """Check if the mandatory fields prompt is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return True
        except:
            return False

    def is_dashboard_header_displayed(self):
        """Check if dashboard header is displayed after login."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except:
            return False

    def is_user_profile_icon_displayed(self):
        """Check if user profile icon is visible after login."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except:
            return False

    # Utility methods for test validation
    def login(self, email, password, remember_me=False):
        """Performs login action with specified credentials and remember me option."""
        self.enter_email(email)
        self.enter_password(password)
        self.set_remember_me(remember_me)
        self.click_login()

    def is_login_successful(self):
        """Checks if login was successful by verifying dashboard header or user profile icon."""
        return self.is_dashboard_header_displayed() or self.is_user_profile_icon_displayed()

    def is_login_error_displayed(self):
        """Checks if error message is displayed indicating invalid credentials."""
        return self.get_error_message() is not None

"""
Documentation:
- All locators and methods are strictly mapped to Locators.json and test case requirements.
- Methods are atomic and reusable for test automation scenarios.
- Utility methods 'login', 'is_login_successful', and 'is_login_error_displayed' simplify test case implementation.
- Exception handling ensures robust test execution and validation.
- All files are placed under the Pages folder as per criteria.
"""
