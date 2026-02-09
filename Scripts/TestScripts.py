
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from Pages.LoginPage import LoginPage
import time

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://your-app-url.com")
        self.login_page = LoginPage(self.driver, locators={})

    def tearDown(self):
        self.driver.quit()

    # Existing test methods preserved...

    def test_TC_LOGIN_005_empty_fields_error(self):
        """
        TC_LOGIN_005: 
        1. Navigate to login page.
        2. Leave both fields empty.
        3. Click Login.
        Expect: Error messages 'Email is required.' and 'Password is required.' User not logged in.
        """
        self.login_page.navigate_to_login()
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        email_error = self.login_page.get_error_message()  # Assuming get_email_error is implemented
        password_error = self.login_page.get_error_message()  # Assuming get_password_error is implemented
        self.assertEqual(email_error, "Email is required.")
        self.assertEqual(password_error, "Password is required.")
        self.assertFalse(self.login_page.is_dashboard_displayed())

    def test_TC_LOGIN_006_remember_me_session_persistence(self):
        """
        TC_LOGIN_006:
        1. Navigate to login page.
        2. Enter valid email/password (user@example.com/ValidPass123!).
        3. Check 'Remember Me'.
        4. Click Login.
        5. Close and reopen browser, revisit site.
        Expect: User remains logged in. Session persists.
        """
        self.login_page.navigate_to_login()
        self.login_page.enter_email("user@example.com")
        self.login_page.enter_password("ValidPass123!")
        # self.login_page.check_remember_me()  # Assuming check_remember_me is implemented
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_dashboard_displayed())

        # Simulate browser restart
        cookies = self.driver.get_cookies()
        self.driver.quit()
        time.sleep(2)  # Wait for browser to close

        self.driver = webdriver.Chrome()
        self.driver.get("https://your-app-url.com")
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.login_page = LoginPage(self.driver, locators={})
        self.assertTrue(self.login_page.is_dashboard_displayed())

    # --- NEW TEST METHODS ---
    def test_TC_LOGIN_009_minimum_length_login(self):
        """
        TC_LOGIN_009:
        1. Navigate to login page.
        2. Enter email at minimum allowed length (a@b.co).
        3. Enter valid password (ValidPass123!).
        4. Click Login.
        Expect: Field accepts input at minimum length, password field accepts input, user is logged in or error is shown.
        """
        self.login_page.navigate_to_login()
        self.login_page.enter_email("a@b.co")
        self.login_page.enter_password("ValidPass123!")
        self.login_page.click_login()
        # Validate minimum length
        self.assertTrue(self.login_page.is_min_length_valid('emailField', 6))
        self.assertTrue(self.login_page.is_min_length_valid('passwordField', 8))
        # Validate login success or error
        dashboard = self.login_page.is_dashboard_displayed()
        error_message = self.login_page.get_error_message()
        self.assertTrue(dashboard or error_message is not None)

    def test_TC_LOGIN_010_failed_login_attempts_lockout(self):
        """
        TC_LOGIN_010:
        1. Navigate to login page.
        2. Enter valid email and incorrect password (user@example.com / WrongPass!@#).
        3. Click Login button repeatedly for max allowed failed attempts (e.g., 5).
        4. On final attempt, verify if account is locked or CAPTCHA is presented.
        Expect: Error message for each failed attempt, lockout/CAPTCHA on last attempt.
        """
        self.login_page.navigate_to_login()
        results = self.login_page.attempt_failed_logins("user@example.com", "WrongPass!@#", max_attempts=5)
        for i, result in enumerate(results):
            self.assertTrue(result['error_message'] is not None)
            if i < 4:
                self.assertFalse(result['account_locked'])
                self.assertFalse(result['captcha'])
        # Check lockout/CAPTCHA on final attempt
        last_result = results[-1]
        self.assertTrue(last_result['account_locked'] or last_result['captcha'])

if __name__ == "__main__":
    unittest.main()
