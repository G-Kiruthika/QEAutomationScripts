# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
verify the absence of the 'Remember Me' checkbox, enter credentials, submit the login form,
and verify error messages as required by TC_LOGIN_001.
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

    def enter_invalid_credentials(self, username: str, password: str):
        """
        Enters invalid username and/or password into the login form.
        :param username: Invalid username string
        :param password: Invalid password string
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Login email field not visible for credential entry."
        )
        password_elem = self.driver.find_element(*self.PASSWORD_FIELD)
        email_elem.clear()
        password_elem.clear()
        email_elem.send_keys(username)
        password_elem.send_keys(password)

    def submit_login_form(self):
        """
        Submits the login form by clicking the login button.
        """
        login_button = self.driver.find_element(*self.LOGIN_SUBMIT_BUTTON)
        login_button.click()

    def verify_error_message(self, expected_message: str) -> bool:
        """
        Verifies that the error message displayed matches the expected message.
        :param expected_message: The expected error message string
        :return: True if the message matches, False otherwise
        """
        error_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE),
            message="Error message not visible after invalid login attempt."
        )
        actual_message = error_elem.text.strip()
        return actual_message == expected_message

# Example usage in a test (not part of the PageClass, for illustration only):
#
# def test_invalid_login(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.enter_invalid_credentials('invalid_user', 'wrong_pass')
#     login_page.submit_login_form()
#     assert login_page.verify_error_message("Invalid username or password. Please try again."), "Error message mismatch"
#
# This will navigate to the login screen, attempt login with invalid credentials, and verify the error message.
