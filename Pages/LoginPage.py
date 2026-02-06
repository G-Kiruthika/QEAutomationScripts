# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
verify the absence of the 'Remember Me' checkbox, and now supports the 'Forgot Username' workflow as required by TC_LOGIN_003.
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
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")  # Assuming locator
    USERNAME_RECOVERY_INPUT = (By.ID, "username-recovery-input")        # Assuming locator
    USERNAME_RECOVERY_SUBMIT = (By.ID, "username-recovery-submit")      # Assuming locator
    USERNAME_RECOVERY_RESULT = (By.CSS_SELECTOR, "div.username-recovery-result") # Assuming locator

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

    # TC_LOGIN_003 additions
    def click_forgot_username_link(self):
        """
        Clicks the 'Forgot Username' link on the login page.
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK),
            message="Forgot Username link not clickable."
        )
        self.driver.find_element(*self.FORGOT_USERNAME_LINK).click()

    def recover_username(self, recovery_info):
        """
        Follows the instructions to recover the username.
        :param recovery_info: The information needed to recover the username (e.g., email or phone)
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.USERNAME_RECOVERY_INPUT),
            message="Username recovery input not visible."
        )
        self.driver.find_element(*self.USERNAME_RECOVERY_INPUT).send_keys(recovery_info)
        self.driver.find_element(*self.USERNAME_RECOVERY_SUBMIT).click()
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.USERNAME_RECOVERY_RESULT),
            message="Username recovery result not visible."
        )
        return self.driver.find_element(*self.USERNAME_RECOVERY_RESULT).text

# Example usage in a test:
# def test_username_recovery(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.click_forgot_username_link()
#     result = login_page.recover_username('user@example.com')
#     assert 'Username retrieved' in result
