# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen
and to verify the absence of the 'Remember Me' checkbox, as required by TC_LOGIN_002.
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

    # --- TC-LOGIN-001: Added Methods Below ---
    def enter_email(self, email: str):
        """
        Enters the provided email address into the email field.
        :param email: Email address to enter
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible on login page."
        )
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password: str):
        """
        Enters the provided password into the password field.
        :param password: Password to enter
        """
        password_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password field not visible on login page."
        )
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        """
        Clicks the Login button to submit the form.
        """
        login_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON),
            message="Login button not clickable on login page."
        )
        login_btn.click()

    def is_dashboard_header_visible(self) -> bool:
        """
        Checks if the dashboard header is visible after login.
        :return: True if dashboard header is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.DASHBOARD_HEADER),
                message="Dashboard header not visible after login."
            )
            return True
        except Exception:
            return False

    def is_user_profile_icon_visible(self) -> bool:
        """
        Checks if the user profile icon is visible after login.
        :return: True if user profile icon is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.USER_PROFILE_ICON),
                message="User profile icon not visible after login."
            )
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """
        Returns the error message text if displayed.
        :return: Error message string, or empty string if not displayed
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_elem.text
        except Exception:
            return ""

    def get_validation_error(self) -> str:
        """
        Returns the validation error text if displayed.
        :return: Validation error string, or empty string if not displayed
        """
        try:
            val_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.VALIDATION_ERROR)
            )
            return val_elem.text
        except Exception:
            return ""

    def is_empty_field_prompt_visible(self) -> bool:
        """
        Checks if the empty field prompt is visible.
        :return: True if prompt is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT)
            )
            return True
        except Exception:
            return False

    # --- End TC-LOGIN-001 Additions ---

# Example usage in a test (not part of the PageClass, for illustration only):
#
# def test_login_success(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.enter_email("testuser@example.com")
#     login_page.enter_password("ValidPass123!")
#     login_page.click_login()
#     assert login_page.is_dashboard_header_visible()
#     assert login_page.is_user_profile_icon_visible()
#
# This will navigate to the login screen, perform login, and verify dashboard/profile icon.
