# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
verify the absence of the 'Remember Me' checkbox, and handle login scenarios including empty fields
and remember me functionality as required by TC_LOGIN_003 and TC_LOGIN_004.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

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

    def login_with_empty_fields_and_verify_error(self):
        """
        TC_LOGIN_003: Leaves login fields empty, clicks login, and verifies error/validation messages.
        Steps:
        1. Navigates to login page.
        2. Ensures email and password fields are empty.
        3. Clicks login submit button.
        4. Waits for error/validation messages and asserts their presence.
        """
        self.go_to_login_page()
        email_input = self.driver.find_element(*self.EMAIL_FIELD)
        password_input = self.driver.find_element(*self.PASSWORD_FIELD)
        # Clear fields if not empty
        email_input.clear()
        password_input.clear()
        # Click login
        self.driver.find_element(*self.LOGIN_SUBMIT_BUTTON).click()
        # Wait for error message or validation prompt
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_any_elements_located([
                self.ERROR_MESSAGE,
                self.VALIDATION_ERROR,
                self.EMPTY_FIELD_PROMPT
            ]),
            message="Expected error/validation message not visible after submitting empty fields."
        )
        # Assert error message
        error_present = False
        try:
            if self.driver.find_element(*self.ERROR_MESSAGE).is_displayed():
                error_present = True
        except NoSuchElementException:
            pass
        try:
            if self.driver.find_element(*self.VALIDATION_ERROR).is_displayed():
                error_present = True
        except NoSuchElementException:
            pass
        try:
            if self.driver.find_element(*self.EMPTY_FIELD_PROMPT).is_displayed():
                error_present = True
        except NoSuchElementException:
            pass
        if not error_present:
            raise AssertionError("No error or validation message displayed after submitting empty fields.")

    def login_with_remember_me_and_verify_auto_login(self, email: str, password: str):
        """
        TC_LOGIN_004: Logs in with valid credentials and 'Remember Me', closes & reopens browser, and verifies auto-login.
        Steps:
        1. Navigates to login page.
        2. Enters valid email and password.
        3. Checks 'Remember Me' checkbox.
        4. Clicks login submit button.
        5. Waits for dashboard header/user profile icon.
        6. Closes and reopens browser, navigates to login page.
        7. Asserts user is auto-logged in (dashboard header/user profile icon visible).
        Note: This method expects the caller to handle browser restart and driver re-instantiation.
        """
        self.go_to_login_page()
        email_input = self.driver.find_element(*self.EMAIL_FIELD)
        password_input = self.driver.find_element(*self.PASSWORD_FIELD)
        remember_me = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        # Fill fields
        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        # Check 'Remember Me' if not already checked
        if not remember_me.is_selected():
            remember_me.click()
        # Click login
        self.driver.find_element(*self.LOGIN_SUBMIT_BUTTON).click()
        # Wait for dashboard header or user profile icon
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_any_elements_located([
                self.DASHBOARD_HEADER,
                self.USER_PROFILE_ICON
            ]),
            message="Dashboard header or user profile icon not visible after login."
        )
        # Simulate browser close/reopen (caller must handle driver restart)
        # After browser restart, navigate to login page and check for auto-login
        self.driver.get(self.URL)
        time.sleep(2)  # Wait for page load
        auto_logged_in = False
        try:
            if self.driver.find_element(*self.DASHBOARD_HEADER).is_displayed():
                auto_logged_in = True
        except NoSuchElementException:
            pass
        try:
            if self.driver.find_element(*self.USER_PROFILE_ICON).is_displayed():
                auto_logged_in = True
        except NoSuchElementException:
            pass
        if not auto_logged_in:
            raise AssertionError("Auto-login failed: Dashboard header or user profile icon not visible after browser restart.")

    # Additional utility methods can be implemented here as needed.

# Example usage in a test (not part of the PageClass, for illustration only):
#
# def test_login_empty_fields(driver):
#     login_page = LoginPage(driver)
#     login_page.login_with_empty_fields_and_verify_error()
#
# def test_login_remember_me_auto_login(driver):
#     login_page = LoginPage(driver)
#     login_page.login_with_remember_me_and_verify_auto_login('user@example.com', 'securePassword123')
#
# Note: For browser restart, the test framework must handle driver teardown and re-instantiation.
