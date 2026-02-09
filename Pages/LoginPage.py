# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
perform login actions, verify error messages, check for the absence of the 'Remember Me' checkbox,
and now supports the 'Forgot Username' workflow as required by TC_LOGIN_003.
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
        self.driver = driver
        self.timeout = timeout

    def go_to_login_page(self):
        self.driver.get(self.URL)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Login email field not visible after navigating to login page."
        )

    def enter_email(self, email: str):
        email_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email input field not visible."
        )
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str):
        password_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password input field not visible."
        )
        password_input.clear()
        password_input.send_keys(password)

    def submit_login(self):
        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON),
            message="Login submit button not clickable."
        )
        login_button.click()

    def is_error_message_displayed(self, expected_text: str = None) -> bool:
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE),
                message="Error message not visible after login attempt."
            )
            if expected_text:
                return expected_text in error_elem.text
            return True
        except NoSuchElementException:
            return False
        except Exception:
            return False

    def is_remember_me_checkbox_present(self) -> bool:
        try:
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
            return True
        except NoSuchElementException:
            return False

    def assert_remember_me_checkbox_absent(self):
        if self.is_remember_me_checkbox_present():
            raise AssertionError(
                "'Remember Me' checkbox should NOT be present on the Login Page, but it was found."
            )

    # TC_LOGIN_003: Forgot Username workflow
    def click_forgot_username_link(self):
        forgot_username_link = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK),
            message="Forgot Username link not clickable."
        )
        forgot_username_link.click()

    def follow_username_recovery_instructions(self):
        # Placeholder for actual recovery steps
        # Example: Wait for instructions page, fill recovery fields, submit, etc.
        recovery_instruction_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.username-recovery-instructions")),
            message="Username recovery instructions not visible."
        )
        # Simulate following instructions
        # Add actual steps as per application flow
        return recovery_instruction_elem.text

    def is_username_retrieved(self) -> bool:
        # Placeholder for actual username retrieval verification
        try:
            username_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.retrieved-username")),
                message="Username not retrieved after recovery."
            )
            return bool(username_elem.text)
        except Exception:
            return False

    # Additional utility methods can be implemented here as needed.
