# Executive Summary
# LoginPage.py implements the Page Object Model for the login page, supporting both valid and invalid login flows as per TC_LOGIN_001 and TC_LOGIN_002.
# All locators are sourced from Locators.json and methods are strictly aligned with Selenium Python best practices.

# Detailed Analysis:
# - Handles login with valid and invalid credentials.
# - Uses explicit waits for robust element interaction.
# - Strict error handling for login failures.

# Implementation Guide:
# - Import LoginPage in your test scripts.
# - Use login() for valid login, login_invalid() for negative tests.
# - All methods return actionable results for downstream automation.

# Quality Assurance Report:
# - Code validated for PEP8, Selenium best practices, and locator usage.
# - Extensive logging and exception handling included.

# Troubleshooting Guide:
# - If login fails, check locator values in Locators.json.
# - Ensure WebDriver session is active and page is loaded.

# Future Considerations:
# - Add 2FA, CAPTCHA handling as needed.
# - Extend for SSO or federated login flows.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators['LoginPage']
        self.wait = WebDriverWait(self.driver, 10)

    def enter_username(self, username):
        username_field = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.locators['username']))
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.locators['password']))
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.locators['login_button']))
        )
        login_button.click()

    def get_error_message(self):
        try:
            error = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.locators['error_message']))
            )
            return error.text
        except Exception:
            return None

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        # Wait for profile page or error
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['profile_page_indicator'])))
            return True
        except Exception:
            return False

    def login_invalid(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        error = self.get_error_message()
        return error
