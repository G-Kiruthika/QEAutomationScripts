# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
enter credentials, perform login, and verify the error message for invalid login attempts as required by TC_LOGIN_001.
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

    # New methods for TC_LOGIN_001
    def enter_credentials(self, email: str, password: str):
        """
        Enters the provided email and password into the login form fields.
        """
        email_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Login email field not visible."
        )
        password_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Login password field not visible."
        )
        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        """
        Clicks the login button to submit the login form.
        """
        login_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON),
            message="Login submit button not clickable."
        )
        login_btn.click()

    def assert_invalid_login_error(self):
        """
        Asserts that the error message for invalid login is displayed.
        """
        error_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE),
            message="Error message not visible after invalid login attempt."
        )
        assert "Invalid username or password. Please try again." in error_elem.text, (
            f"Expected error message not found. Actual: {error_elem.text}"
        )

# Example test for TC_LOGIN_001 (not part of the PageClass, for illustration only):
# def test_invalid_login(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.enter_credentials("invalid_user", "invalid_pass")
#     login_page.click_login()
#     login_page.assert_invalid_login_error()
