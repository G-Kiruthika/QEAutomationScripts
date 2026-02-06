# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
verify the absence of the 'Remember Me' checkbox, enter invalid credentials, and verify the error message for invalid login attempts as required by TC_LOGIN_001 and TC_LOGIN_002.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
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

    def enter_invalid_credentials_and_submit(self, invalid_username: str, invalid_password: str):
        """
        Enters invalid username and password and submits the login form.
        """
        email_elem = self.driver.find_element(*self.EMAIL_FIELD)
        password_elem = self.driver.find_element(*self.PASSWORD_FIELD)
        email_elem.clear()
        password_elem.clear()
        email_elem.send_keys(invalid_username)
        password_elem.send_keys(invalid_password)
        self.driver.find_element(*self.LOGIN_SUBMIT_BUTTON).click()

    def verify_error_message_for_invalid_login(self) -> bool:
        """
        Verifies that the error message for invalid login is displayed.
        :return: True if correct error message is displayed, False otherwise
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE),
                message="Error message not visible after invalid login attempt."
            )
            return "Invalid username or password. Please try again." in error_elem.text
        except (NoSuchElementException, Exception):
            return False

# Example usage in a test (not part of the PageClass, for illustration only):
#
# def test_invalid_login(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.enter_invalid_credentials_and_submit("wronguser", "wrongpass")
#     assert login_page.verify_error_message_for_invalid_login()
#
# This will navigate to the login screen, enter invalid credentials, and verify the error message.
