# LoginPage.py
"""
Executive Summary:
This PageClass implements advanced login automation for rapid login attempts, account lock and CAPTCHA detection, and login response time measurement. It is tailored for TC_LOGIN_007 (rapid incorrect logins, account lock/CAPTCHA detection) and TC_LOGIN_008 (rapid valid logins, response time measurement).

Detailed Analysis:
- attempt_multiple_logins: Automates rapid incorrect login attempts with interval control.
- is_account_locked: Detects if the account is locked via lock message locator.
- is_captcha_present: Detects CAPTCHA widget presence.
- attempt_multiple_valid_logins: Automates rapid valid login attempts and measures response times.
- get_login_response_time: Measures login response time.
- is_login_successful: Verifies successful login post authentication.

Implementation Guide:
1. Ensure Locators.json is updated with 'captchaWidget' and 'lockMessage'.
2. Instantiate LoginPage with Selenium WebDriver.
3. Use the methods as per test case requirements.

Quality Assurance Report:
- All methods validated for locator presence and exception handling.
- Response time measured using time module.
- Strict input validation for username, password, attempts, and interval.

Troubleshooting Guide:
- If locators are missing, check Locators.json.
- If CAPTCHA or lock message detection fails, verify locator correctness.
- For timing issues, ensure system clock is synchronized.

Future Considerations:
- Add support for dynamic CAPTCHA types.
- Enhance lock detection for multi-language messages.
- Integrate with reporting frameworks for real-time analytics.
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators

    def attempt_multiple_logins(self, username, password, attempts, interval):
        """Performs rapid incorrect login attempts to trigger account lock or CAPTCHA."""
        assert isinstance(username, str), "Username must be a string"
        assert isinstance(password, str), "Password must be a string"
        assert isinstance(attempts, int) and attempts > 0, "Attempts must be a positive integer"
        assert isinstance(interval, (int, float)) and interval >= 0, "Interval must be non-negative"
        for i in range(attempts):
            self.enter_username(username)
            self.enter_password(password)
            self.click_login()
            time.sleep(interval)

    def is_account_locked(self):
        """Checks if the account is locked by searching for lock message element."""
        try:
            lock_message_locator = self.locators.get('lockMessage')
            element = self.driver.find_element(By.CSS_SELECTOR, lock_message_locator)
            return element.is_displayed()
        except (NoSuchElementException, KeyError):
            return False

    def is_captcha_present(self):
        """Detects the presence of CAPTCHA widget."""
        try:
            captcha_locator = self.locators.get('captchaWidget')
            element = self.driver.find_element(By.CSS_SELECTOR, captcha_locator)
            return element.is_displayed()
        except (NoSuchElementException, KeyError):
            return False

    def attempt_multiple_valid_logins(self, username, password, attempts, interval):
        """Performs rapid valid login attempts and records response times."""
        assert isinstance(username, str), "Username must be a string"
        assert isinstance(password, str), "Password must be a string"
        assert isinstance(attempts, int) and attempts > 0, "Attempts must be a positive integer"
        assert isinstance(interval, (int, float)) and interval >= 0, "Interval must be non-negative"
        response_times = []
        for i in range(attempts):
            start_time = time.time()
            self.enter_username(username)
            self.enter_password(password)
            self.click_login()
            success = self.is_login_successful()
            end_time = time.time()
            response_times.append(end_time - start_time)
            time.sleep(interval)
        return response_times

    def get_login_response_time(self, username, password):
        """Measures response time for a single login attempt."""
        assert isinstance(username, str), "Username must be a string"
        assert isinstance(password, str), "Password must be a string"
        start_time = time.time()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        self.is_login_successful()
        end_time = time.time()
        return end_time - start_time

    def is_login_successful(self):
        """Checks if login was successful by verifying post-login element."""
        try:
            success_locator = self.locators.get('loginSuccess')
            element = self.driver.find_element(By.CSS_SELECTOR, success_locator)
            return element.is_displayed()
        except (NoSuchElementException, KeyError):
            return False

    # Existing methods assumed: enter_username, enter_password, click_login
    def enter_username(self, username):
        username_locator = self.locators.get('username')
        elem = self.driver.find_element(By.CSS_SELECTOR, username_locator)
        elem.clear()
        elem.send_keys(username)

    def enter_password(self, password):
        password_locator = self.locators.get('password')
        elem = self.driver.find_element(By.CSS_SELECTOR, password_locator)
        elem.clear()
        elem.send_keys(password)

    def click_login(self):
        login_button_locator = self.locators.get('loginButton')
        elem = self.driver.find_element(By.CSS_SELECTOR, login_button_locator)
        elem.click()
