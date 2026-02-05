# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
perform login actions, and verify error messages for invalid login attempts as required by TC_LOGIN_001 and TC_LOGIN_002.
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
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")  # Added for TC_LOGIN_003
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

    def login(self, username: str, password: str):
        """
        Enters the provided username and password and submits the login form.
        :param username: Username or email to enter
        :param password: Password to enter
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible for login."
        )
        password_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password field not visible for login."
        )
        email_elem.clear()
        email_elem.send_keys(username)
        password_elem.clear()
        password_elem.send_keys(password)
        submit_btn = self.driver.find_element(*self.LOGIN_SUBMIT_BUTTON)
        submit_btn.click()

    def assert_invalid_login_error_message(self, expected_message: str = "Invalid username or password. Please try again."):
        """
        Asserts that the invalid login error message is displayed and matches the expected text.
        :param expected_message: The expected error message text
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE),
                message="Error message not visible after invalid login attempt."
            )
            actual_message = error_elem.text.strip()
            assert actual_message == expected_message, (
                f"Expected error message '{expected_message}', but got '{actual_message}'."
            )
        except TimeoutException:
            raise AssertionError("Error message not displayed after invalid login attempt.")

    def click_forgot_username_link(self):
        """
        Clicks the 'Forgot Username' link to initiate the username recovery workflow (TC_LOGIN_003).
        Navigates to the Forgot Username page.
        """
        link = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK),
            message="'Forgot Username' link not clickable on Login Page."
        )
        link.click()

# Example usage in a test (not part of the PageClass, for illustration only):
#
# def test_invalid_login_error(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.login("invalid_user", "invalid_pass")
#     login_page.assert_invalid_login_error_message()
#
# This will navigate to the login screen, attempt an invalid login, and verify the error message as required by TC_LOGIN_001.
