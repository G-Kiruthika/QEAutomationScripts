# ForgotUsernamePage.py
"""
Page Object Model for the Forgot Username Page
Author: [Your Name]
Description: Encapsulates interactions and verifications for the Forgot Username (username recovery) workflow as required by TC_LOGIN_003.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ForgotUsernamePage:
    """
    Page Object for the Forgot Username (Username Recovery) Screen
    """

    # Locators (assumed based on standard UI patterns; update with actual values as needed)
    EMAIL_FIELD = (By.ID, "recovery-email")  # The email input to identify the user
    SUBMIT_BUTTON = (By.ID, "recovery-submit")  # Button to request username recovery
    INSTRUCTION_TEXT = (By.CSS_SELECTOR, "div.recovery-instructions")  # Instructions for recovery
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert-success")  # Success message after submission
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")  # Error message for invalid input

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initializes the ForgotUsernamePage with a Selenium WebDriver instance.
        :param driver: Selenium WebDriver
        :param timeout: Default wait timeout for elements
        """
        self.driver = driver
        self.timeout = timeout

    def is_loaded(self) -> bool:
        """
        Checks if the Forgot Username page is loaded by verifying presence of instruction text or email field.
        :return: True if loaded, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.EMAIL_FIELD),
                message="Forgot Username email field not visible."
            )
            return True
        except TimeoutException:
            return False

    def enter_email_and_submit(self, email: str):
        """
        Enters the given email address and submits the username recovery form.
        :param email: Email address associated with the account
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible on Forgot Username page."
        )
        email_elem.clear()
        email_elem.send_keys(email)
        submit_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON),
            message="Submit button not clickable on Forgot Username page."
        )
        submit_btn.click()

    def assert_success_message(self, expected_message: str = "Your username has been sent to your email address."):
        """
        Asserts that the success message is displayed and matches the expected text.
        :param expected_message: Expected message after successful recovery
        """
        try:
            success_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE),
                message="Success message not visible after username recovery."
            )
            actual_message = success_elem.text.strip()
            assert actual_message == expected_message, (
                f"Expected success message '{expected_message}', but got '{actual_message}'."
            )
        except TimeoutException:
            raise AssertionError("Success message not displayed after username recovery.")

    def assert_error_message(self, expected_message: str):
        """
        Asserts that the error message is displayed and matches the expected text.
        :param expected_message: Expected error message
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE),
                message="Error message not visible after invalid recovery attempt."
            )
            actual_message = error_elem.text.strip()
            assert actual_message == expected_message, (
                f"Expected error message '{expected_message}', but got '{actual_message}'."
            )
        except TimeoutException:
            raise AssertionError("Error message not displayed after invalid username recovery attempt.")
