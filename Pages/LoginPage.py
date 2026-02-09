# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
enter credentials, submit login, verify dashboard, and verify error messages.
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

    def enter_username(self, username: str):
        """
        Enters the username (email) into the email field.
        """
        email_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD)
        )
        email_input.clear()
        email_input.send_keys(username)

    def enter_password(self, password: str):
        """
        Enters the password into the password field.
        """
        password_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)
        )
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        """
        Clicks the login button to submit credentials.
        """
        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON)
        )
        login_button.click()

    def is_dashboard_displayed(self) -> bool:
        """
        Checks if the dashboard header is displayed after successful login.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.DASHBOARD_HEADER)
            )
            return True
        except Exception:
            return False

    def is_error_message_displayed(self) -> bool:
        """
        Checks if error message is displayed after invalid login.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return True
        except Exception:
            return False

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

    def get_error_message_text(self) -> str:
        """
        Returns the error message text displayed for invalid login.
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_elem.text
        except Exception:
            return ""

    # Additional utility methods can be implemented here as needed.

# Example usage in a test (not part of the PageClass, for illustration only):
#
# def test_valid_login(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.enter_username('user1')
#     login_page.enter_password('Pass@123')
#     login_page.click_login()
#     assert login_page.is_dashboard_displayed(), "Dashboard not displayed after login"
#
# def test_invalid_login(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.enter_username('invalidUser')
#     login_page.enter_password('WrongPass')
#     login_page.click_login()
#     assert login_page.is_error_message_displayed(), "Error message not displayed for invalid login"
