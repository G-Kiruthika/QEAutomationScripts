# LoginPage.py
"""
Page Object for Login Page.
Supports login, forgot password, and forgot username workflows.
Strictly follows Selenium Python best practices.

Test Case Supported: TC_LOGIN_003 - Forgot Username workflow.

Author: QEAutomation Orchestration Agent
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for the Login Page.
    """
    URL = "https://example-ecommerce.com/login"

    # Locators (from Locators/Locators.json)
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    # Assumption: Adding a locator for 'Forgot Username' link since not present in Locators.json
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")  # TODO: Update selector as per application
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        """Navigate to the login page."""
        self.driver.get(self.URL)

    def click_forgot_username(self):
        """
        Clicks the 'Forgot Username' link to initiate username recovery workflow.
        Returns True if link is found and clicked, raises TimeoutException otherwise.
        """
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
        link.click()
        return True

    def recover_username(self, email):
        """
        Follows instructions to recover username.
        Assumes a modal or new page appears with an input for email and a submit button.
        This is a template; selectors should be updated based on actual UI.
        """
        # Example locators for recovery workflow (should be updated as per actual UI)
        RECOVERY_EMAIL_FIELD = (By.ID, "recovery-email")
        RECOVERY_SUBMIT_BUTTON = (By.ID, "recovery-submit")
        USERNAME_RESULT = (By.CSS_SELECTOR, "span.recovered-username")

        email_input = self.wait.until(EC.visibility_of_element_located(RECOVERY_EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)
        submit_btn = self.wait.until(EC.element_to_be_clickable(RECOVERY_SUBMIT_BUTTON))
        submit_btn.click()
        username_elem = self.wait.until(EC.visibility_of_element_located(USERNAME_RESULT))
        return username_elem.text

    # Existing methods (login, etc.) should remain unaltered.
    # Add new methods below this line for extensibility.

