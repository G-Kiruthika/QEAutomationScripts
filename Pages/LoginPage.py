# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
verify the absence/presence of the 'Remember Me' checkbox, handle login scenarios including
empty fields and 'Remember Me', and validate post-login states as required by TC_LOGIN_003 and TC_LOGIN_004.

Quality Assurance:
- All methods include explicit waits for element visibility.
- Exception handling is present for element lookup and assertions.
- Code is structured for maintainability and extensibility.

Troubleshooting:
- If locators change, update the locator definitions.
- If error messages are not displayed, check for dynamic content or AJAX delays.
- For 'Remember Me' functionality, ensure cookies/session handling is enabled in test environment.

Future Considerations:
- Extend with multi-language support for messages.
- Add logging and screenshot capture for failed assertions.
- Modularize repeated actions for DRY principle.
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

    # --- TC_LOGIN_003 Implementation ---
    def clear_login_fields(self):
        """
        Clears the username and password fields.
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible for clearing."
        )
        password_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password field not visible for clearing."
        )
        email_elem.clear()
        password_elem.clear()

    def click_login_button(self):
        """
        Clicks the Login button.
        """
        login_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON),
            message="Login button not clickable."
        )
        login_btn.click()

    def is_error_message_displayed(self) -> bool:
        """
        Checks if the error message prompting to fill required fields is displayed.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return True
        except TimeoutException:
            return False

    def get_error_message_text(self) -> str:
        """
        Returns the error message text if displayed.
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_elem.text
        except TimeoutException:
            return ""

    # --- TC_LOGIN_004 Implementation ---
    def enter_credentials(self, username: str, password: str):
        """
        Enters the provided username and password in the login fields.
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible for entering username."
        )
        password_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password field not visible for entering password."
        )
        email_elem.clear()
        email_elem.send_keys(username)
        password_elem.clear()
        password_elem.send_keys(password)

    def check_remember_me(self):
        """
        Checks the 'Remember Me' checkbox if it is present and not already checked.
        """
        try:
            checkbox = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX)
            )
            if not checkbox.is_selected():
                checkbox.click()
        except TimeoutException:
            raise AssertionError("'Remember Me' checkbox not found or not clickable.")

    def is_logged_in(self) -> bool:
        """
        Verifies if the user is logged in by checking for dashboard header or user profile icon.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.DASHBOARD_HEADER)
            )
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.USER_PROFILE_ICON)
            )
            return True
        except TimeoutException:
            return False

    def assert_user_auto_logged_in(self):
        """
        Asserts that user remains logged in or is auto-logged in after browser reopen.
        """
        if not self.is_logged_in():
            raise AssertionError("User is not auto-logged in after reopening browser.")

    # Additional utility methods can be implemented here as needed.

# Example usage for TC_LOGIN_003:
# login_page = LoginPage(driver)
# login_page.go_to_login_page()
# login_page.clear_login_fields()
# login_page.click_login_button()
# assert login_page.is_error_message_displayed(), "Error message not shown for empty fields"
#
# Example usage for TC_LOGIN_004:
# login_page.go_to_login_page()
# login_page.enter_credentials("user1", "Pass@123")
# login_page.check_remember_me()
# login_page.click_login_button()
# assert login_page.is_logged_in(), "User not logged in after valid credentials"
# # Close/reopen browser, navigate to login page
# login_page.go_to_login_page()
# login_page.assert_user_auto_logged_in()
