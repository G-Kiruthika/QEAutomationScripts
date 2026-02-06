"""
ForgotUsernamePage.py
Page Object Model for the Forgot Username Workflow
Author: [Your Name]
Description: Encapsulates the interactions and verifications for the 'Forgot Username' workflow as required by TC_LOGIN_003.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class ForgotUsernamePage:
    """
    Page Object for the Forgot Username Workflow
    """

    # Locators (Assumed based on standard application conventions)
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")
    INSTRUCTIONS_CONTAINER = (By.CSS_SELECTOR, "div.forgot-username-instructions")
    EMAIL_INPUT = (By.ID, "forgot-username-email")
    SUBMIT_BUTTON = (By.ID, "forgot-username-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initializes the ForgotUsernamePage with a Selenium WebDriver instance.
        :param driver: Selenium WebDriver
        :param timeout: Default wait timeout for elements
        """
        self.driver = driver
        self.timeout = timeout

    def click_forgot_username_link(self):
        """
        Clicks the 'Forgot Username' link on the login page and waits for instructions to appear.
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK),
            message="'Forgot Username' link is not clickable."
        )
        self.driver.find_element(*self.FORGOT_USERNAME_LINK).click()
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.INSTRUCTIONS_CONTAINER),
            message="Instructions for recovering username did not appear."
        )

    def follow_recovery_instructions(self, email: str):
        """
        Follows the instructions to recover username by entering the email and submitting the form.
        :param email: Registered email address
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_INPUT),
            message="Email input for username recovery is not visible."
        )
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON),
            message="Submit button for username recovery is not clickable."
        )
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def is_username_retrieved(self) -> bool:
        """
        Checks if the username retrieval was successful by verifying the success message.
        :return: True if success message is displayed, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE),
                message="Success message not displayed after username recovery."
            )
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """
        Retrieves any error message displayed during the username recovery process.
        :return: Error message text if displayed, else empty string
        """
        try:
            error_element = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_element.text
        except NoSuchElementException:
            return ""

# Example usage in a test (not part of the PageClass):
#
# def test_forgot_username_workflow(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     forgot_username_page = ForgotUsernamePage(driver)
#     forgot_username_page.click_forgot_username_link()
#     forgot_username_page.follow_recovery_instructions(email="user@example.com")
#     assert forgot_username_page.is_username_retrieved(), "Username was not retrieved successfully."
