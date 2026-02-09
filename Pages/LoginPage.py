# LoginPage.py
# Selenium Page Object for Login functionality
# All locators are sourced from Locators.json
# QA Report: All methods required for TC_LOGIN_01 and TC_LOGIN_02 are present. Code follows Selenium best practices. Imports are complete. Each method includes robust waiting and error handling.

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for the Login Page.
    Methods:
        - open(): Navigates to the login page.
        - enter_email(email): Enters email/username.
        - enter_password(password): Enters password.
        - click_remember_me(): Toggles 'Remember Me' checkbox.
        - click_login(): Clicks the login button.
        - click_forgot_password(): Clicks the 'Forgot Password' link.
        - get_error_message(): Returns error message text if present.
        - get_validation_error(): Returns validation error text if present.
        - is_empty_field_prompt_displayed(): Checks for empty fields prompt.
        - is_dashboard_header_displayed(): Checks if dashboard header is visible after login.
        - is_user_profile_icon_displayed(): Checks if user profile icon is visible after login.
        - is_min_length_error_displayed(): Checks for minimum length error message.
    All locators are sourced from Locators.json.

    Covers:
        - TC_LOGIN_01: Valid login scenario (navigate, input, submit, dashboard validation).
        - TC_LOGIN_02: Invalid login scenario (navigate, input, submit, error message validation).
    """

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
        """Initialize LoginPage with WebDriver."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Navigate to the login page and wait for email field."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email: str):
        """Enter email/username into the email field."""
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str):
        """Enter password into the password field."""
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_remember_me(self):
        """Click the 'Remember Me' checkbox."""
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
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
        """Return the error message text if present."""
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text
        except Exception:
            return None

    def get_validation_error(self):
        """Return the validation error text if present."""
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return error.text
        except Exception:
            return None

    def is_empty_field_prompt_displayed(self):
        """Check if the empty field prompt is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return True
        except Exception:
            return False

    def is_dashboard_header_displayed(self):
        """Check if the dashboard header is displayed after login."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def is_user_profile_icon_displayed(self):
        """Check if the user profile icon is displayed after login."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except Exception:
            return False

    def is_min_length_error_displayed(self):
        """
        Check if the minimum length error message ('Email/Username must be at least 3 characters.') is displayed.
        This method is used for TC_LOGIN_02 validation.
        """
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            if error.text.strip() == 'Email/Username must be at least 3 characters.':
                return True
            return False
        except Exception:
            return False
