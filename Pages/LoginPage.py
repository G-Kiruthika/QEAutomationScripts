# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen
and to verify the absence of the 'Remember Me' checkbox, as required by TC_LOGIN_002.

---

Executive Summary:
This update introduces new methods to the LoginPage Page Object for handling navigation, empty fields validation, error message detection, 'Remember Me' functionality, and session persistence as required by test cases TC_LOGIN_003 and TC_LOGIN_004. Existing logic remains unaltered; new code is appended for enhanced automation coverage.

Detailed Analysis:
- TC_LOGIN_003: Requires navigation, empty fields validation, and error message detection.
- TC_LOGIN_004: Requires navigation, valid credentials entry, 'Remember Me' functionality, login action, and session persistence across browser sessions.
Locators used are defined within the class, ensuring element integrity and maintainability.

Implementation Guide:
- Use go_to_login_page() for navigation.
- Use leave_fields_empty_and_validate() to clear fields and check empty state.
- Use click_login_and_check_empty_error() to submit empty fields and verify error prompt.
- Use login_with_remember_me() to login with 'Remember Me' checked.
- Use check_session_persistence() to verify user remains logged in after browser restart.

Quality Assurance Report:
- All methods include waits and exception handling.
- Element locators are strictly used as defined in the class.
- No existing logic is altered; only new, append-only code is introduced.
- Each method is independently testable and supports downstream automation.

Troubleshooting Guide:
- If elements are not found, ensure page loads and locators are correct.
- For session persistence, browser cookies must be preserved or managed between sessions.
- Error message checks rely on visible prompts; adjust locator if UI changes.

Future Considerations:
- Expand methods for additional login scenarios (e.g., multi-factor, social logins).
- Integrate with test data management for dynamic credential handling.
- Refactor for cross-browser and mobile compatibility as needed.

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

    # --- TC_LOGIN_003 ---
    def leave_fields_empty_and_validate(self):
        """
        Clears the username and password fields and validates that they are empty.
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible for empty validation."
        )
        password_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password field not visible for empty validation."
        )
        email_elem.clear()
        password_elem.clear()
        assert email_elem.get_attribute("value") == "", "Email field should be empty."
        assert password_elem.get_attribute("value") == "", "Password field should be empty."

    def click_login_and_check_empty_error(self):
        """
        Clicks the login button with empty fields and verifies the error message for required fields.
        """
        login_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON),
            message="Login button not clickable for empty fields error check."
        )
        login_btn.click()
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT),
                message="Mandatory fields error prompt not visible."
            )
        except TimeoutException:
            raise AssertionError("Error message for empty fields not displayed.")

    # --- TC_LOGIN_004 ---
    def login_with_remember_me(self, username: str, password: str):
        """
        Enters valid credentials, checks 'Remember Me', and clicks login.
        :param username: Username string
        :param password: Password string
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible for login."
        )
        password_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password field not visible for login."
        )
        remember_me_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX),
            message="'Remember Me' checkbox not visible."
        )
        email_elem.clear()
        email_elem.send_keys(username)
        password_elem.clear()
        password_elem.send_keys(password)
        if not remember_me_elem.is_selected():
            remember_me_elem.click()
        assert remember_me_elem.is_selected(), "'Remember Me' checkbox should be checked."
        login_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON),
            message="Login button not clickable for login."
        )
        login_btn.click()
        # Wait for dashboard or user profile icon indicating successful login
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.DASHBOARD_HEADER),
            message="Dashboard header not visible after login."
        )

    def check_session_persistence(self):
        """
        Checks if the user session persists after browser is reopened and navigated to the site.
        """
        # This method assumes cookies/session storage are preserved externally by the test framework.
        self.driver.get(self.URL)
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.USER_PROFILE_ICON),
                message="User profile icon not visible, user not logged in after browser restart."
            )
        except TimeoutException:
            raise AssertionError("Session did not persist after browser restart; user not auto-logged in.")

# Example usage in a test (not part of the PageClass, for illustration only):
#
# def test_empty_fields_error(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.leave_fields_empty_and_validate()
#     login_page.click_login_and_check_empty_error()
#
# def test_remember_me_session(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.login_with_remember_me("user1", "Pass@123")
#     # Simulate browser close/reopen and restore cookies/session
#     login_page.check_session_persistence()
