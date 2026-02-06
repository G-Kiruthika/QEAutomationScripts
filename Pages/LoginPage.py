# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. Now supports TC_LOGIN_001: navigation, credential entry,
login submission, and error message verification.

Update for TC_LOGIN_002:
- Adds explicit documentation and method usage for verifying absence of 'Remember Me' checkbox as per test steps.

Update for TC_LOGIN_003:
- Implements 'Forgot Username' workflow: navigation, verification, link click, recovery, and confirmation.
- All new logic is appended; no existing logic is altered.
- Comprehensive documentation and QA report included at the end of this file.
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

    # --- TC_LOGIN_003 Locators (custom, as Locators.json lacks explicit 'Forgot Username') ---
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")  # Assumed selector
    USERNAME_RECOVERY_INSTRUCTIONS = (By.CSS_SELECTOR, "div.username-recovery-instructions")  # Assumed selector
    USERNAME_RESULT = (By.CSS_SELECTOR, "span.recovered-username")  # Assumed selector

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

    def enter_email(self, email: str):
        """
        Enters the provided email into the email field.
        """
        email_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Email field not visible."
        )
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password: str):
        """
        Enters the provided password into the password field.
        """
        password_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD),
            message="Password field not visible."
        )
        password_elem.clear()
        password_elem.send_keys(password)

    def submit_login(self):
        """
        Clicks the login submit button.
        """
        submit_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON),
            message="Login submit button not clickable."
        )
        submit_btn.click()

    def get_error_message(self) -> str:
        """
        Returns the error message displayed after login attempt.
        :return: Error message text or empty string if not present.
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE),
                message="Error message not visible."
            )
            return error_elem.text.strip()
        except (TimeoutException, NoSuchElementException):
            return ""

    def assert_error_message(self, expected_message: str):
        """
        Asserts that the error message matches the expected text.
        Raises AssertionError if not matched.
        """
        actual_message = self.get_error_message()
        if actual_message != expected_message:
            raise AssertionError(
                f"Expected error message: '{expected_message}', but got: '{actual_message}'"
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

    # --- TC_LOGIN_002 Implementation ---
    def run_tc_login_002(self):
        """
        Implements Test Case TC_LOGIN_002:
        1. Navigates to the login screen.
        2. Verifies that the login screen is displayed.
        3. Checks for the presence of 'Remember Me' checkbox and asserts its absence.
        """
        self.go_to_login_page()
        # Step 2: Verify login screen is displayed (email field visible)
        if not WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.EMAIL_FIELD)):
            raise AssertionError("Login screen is not displayed.")
        # Step 3: Assert 'Remember Me' checkbox is NOT present
        self.assert_remember_me_checkbox_absent()

    # --- TC_LOGIN_003 Implementation ---
    def run_tc_login_003(self, recovery_email: str = None) -> str:
        """
        Implements Test Case TC_LOGIN_003: Forgot Username Workflow
        Steps:
        1. Navigate to login screen
        2. Verify login screen is displayed
        3. Click 'Forgot Username' link
        4. Follow instructions to recover username
        5. Confirm username is retrieved
        :param recovery_email: Email to be used for recovery (if required by workflow)
        :return: The recovered username
        """
        self.go_to_login_page()
        # Step 2: Verify login screen is displayed
        if not WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.EMAIL_FIELD)):
            raise AssertionError("Login screen is not displayed.")
        # Step 3: Click 'Forgot Username' link
        try:
            forgot_username_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK),
                message="'Forgot Username' link not clickable."
            )
            forgot_username_elem.click()
        except TimeoutException:
            raise AssertionError("'Forgot Username' link not found on Login Page.")
        # Step 4: Follow instructions to recover username
        try:
            instructions_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.USERNAME_RECOVERY_INSTRUCTIONS),
                message="Username recovery instructions not visible."
            )
        except TimeoutException:
            raise AssertionError("Username recovery instructions not displayed.")
        # If email entry required, fill it
        if recovery_email:
            try:
                recovery_email_field = self.driver.find_element(By.ID, "recovery-email")
                recovery_email_field.clear()
                recovery_email_field.send_keys(recovery_email)
                # Assume a submit button for recovery
                recovery_submit_btn = self.driver.find_element(By.ID, "recovery-submit")
                recovery_submit_btn.click()
            except NoSuchElementException:
                raise AssertionError("Recovery email field or submit button not found.")
        # Step 5: Confirm username is retrieved
        try:
            username_result_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.USERNAME_RESULT),
                message="Recovered username not displayed."
            )
            recovered_username = username_result_elem.text.strip()
            if not recovered_username:
                raise AssertionError("Recovered username is empty.")
        except TimeoutException:
            raise AssertionError("Recovered username not found after recovery.")
        return recovered_username

    def is_forgot_username_link_present(self) -> bool:
        """
        Checks if the 'Forgot Username' link is present on the login page.
        :return: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.FORGOT_USERNAME_LINK)
            return True
        except NoSuchElementException:
            return False

    def assert_forgot_username_link_present(self):
        """
        Asserts that the 'Forgot Username' link is present on the login page.
        Raises AssertionError if the link is not found.
        """
        if not self.is_forgot_username_link_present():
            raise AssertionError("'Forgot Username' link is NOT present on the Login Page.")

"""
QA Report for TC_LOGIN_003 Implementation
----------------------------------------
1. Code Integrity: Existing logic is strictly preserved. All new code is appended at the end of LoginPage class.
2. Imports: All necessary Selenium imports are present and reused. No redundant imports added.
3. Locators: 'Forgot Username' workflow uses assumed selectors due to absence in Locators.json. These are:
   - FORGOT_USERNAME_LINK: (By.CSS_SELECTOR, "a.forgot-username-link")
   - USERNAME_RECOVERY_INSTRUCTIONS: (By.CSS_SELECTOR, "div.username-recovery-instructions")
   - USERNAME_RESULT: (By.CSS_SELECTOR, "span.recovered-username")
   If actual selectors differ, update Locators.json and this file accordingly.
4. Documentation: All new methods are fully documented with stepwise explanations and parameter details.
5. Workflow Validation:
   - Navigation and screen verification use explicit waits.
   - Link presence and clickability are validated.
   - Recovery instructions and result are checked with robust error handling.
   - Optional email entry is supported for flexible workflows.
6. Output Structure: The file is committed as a JSON array with 'path' and 'content' for downstream automation.
7. Best Practices: All waits are explicit; exceptions are handled; code is modular and readable.
8. Manual QA Needed: Confirm actual selectors for 'Forgot Username' workflow in the app UI and update as needed.
"""
