# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. Now supports TC_LOGIN_001: navigation, credential entry,
login submission, and error message verification.

Update for TC_LOGIN_002:
- Adds explicit documentation and method usage for verifying absence of 'Remember Me' checkbox as per test steps.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for the Login Screen
    """

    # Locators (from Locators.json)
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initializes the LoginPage with a Selenium WebDriver instance.
        :param driver: Selenium WebDriver
        :param timeout: Default wait timeout for elements
        """
        self.driver = driver
        self.timeout = timeout

    def go_to_login_page(self):
        """
        Navigates the browser to the login page URL and waits for the login form to be visible.
        """
        self.driver.get(self.URL)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Login email field not visible after navigating to login page."
        )

    def enter_email(self, email: str):
        """
        Enters the provided email into the email field.
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible."
        )
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password: str):
        """
        Enters the provided password into the password field.
        """
        password_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password field not visible."
        )
        password_elem.clear()
        password_elem.send_keys(password)

    def submit_login(self):
        """
        Clicks the login submit button.
        """
        submit_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON),
            message="Login submit button not clickable."
        )
        submit_btn.click()

    def get_error_message(self) -> str:
        """
        Returns the error message displayed after login attempt.
        :return: Error message text or empty string if not present.
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE),
                message="Error message not visible."
            )
            return error_elem.text.strip()
        except (TimeoutException, NoSuchElementException):
            return ""

    def assert_error_message(self, expected_message: str):
        """
        Asserts that the error message matches the expected text.
        Raises AssertionError if not matched.
        """
        actual_message = self.get_error_message()
        if actual_message != expected_message:
            raise AssertionError(
                f"Expected error message: '{expected_message}', but got: '{actual_message}'"
            )

    def is_remember_me_checkbox_present(self) -> bool:
        """
        Checks if the 'Remember Me' checkbox is present on the login page.
        :return: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
            return True
        except NoSuchElementException:
            return False

    def assert_remember_me_checkbox_absent(self):
        """
        Asserts that the 'Remember Me' checkbox is NOT present on the login page.
        Raises AssertionError if the checkbox is found.
        """
        if self.is_remember_me_checkbox_present():
            raise AssertionError(
                "'Remember Me' checkbox should NOT be present on the Login Page, but it was found."
            )

    # --- TC_LOGIN_002 Implementation ---
    def run_tc_login_002(self):
        """
        Implements Test Case TC_LOGIN_002:
        1. Navigates to the login screen.
        2. Verifies that the login screen is displayed.
        3. Checks for the presence of 'Remember Me' checkbox and asserts its absence.
        """
        self.go_to_login_page()
        # Step 2: Verify login screen is displayed (email field visible)
        if not WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.EMAIL_FIELD)):
            raise AssertionError("Login screen is not displayed.")
        # Step 3: Assert 'Remember Me' checkbox is NOT present
        self.assert_remember_me_checkbox_absent()
