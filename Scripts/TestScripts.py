import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLoginFunctionality(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC_LOGIN_009_minimum_length_email(self):
        """
        TC_LOGIN_009: Verify login with minimum allowed length email/username.
        Steps:
        1. Navigate to the login page.
        2. Enter email 'a@b.co' and password 'ValidPass123!'.
        3. Click Login.
        4. Assert dashboard is visible or error message is shown.
        """
        self.login_page.navigate()
        result = self.login_page.login_with_minimum_length_email('a@b.co', 'ValidPass123!')
        self.assertTrue(result['dashboard_visible'] or result['error_message'] is not None, 'User should be logged in or see an error message.')

    def test_TC_LOGIN_010_failed_attempts_and_lockout(self):
        """
        TC_LOGIN_010: Verify account lockout or CAPTCHA after maximum failed login attempts.
        Steps:
        1. Navigate to the login page.
        2. Enter valid email 'user@example.com' and incorrect password 'WrongPass!@#'.
        3. Click Login 5 times.
        4. Assert error message is displayed for each failed attempt.
        5. On final attempt, assert account is locked or CAPTCHA is displayed.
        """
        self.login_page.navigate()
        results = self.login_page.login_with_failed_attempts('user@example.com', 'WrongPass!@#', max_attempts=5)
        for attempt in results:
            self.assertIsNotNone(attempt['error_message'], f"Attempt {attempt['attempt']}: Error message should be shown.")
        # Check for lockout or CAPTCHA on last attempt
        last_attempt = results[-1]
        self.assertTrue(last_attempt['account_locked'] or last_attempt['captcha_displayed'], 'Account should be locked or CAPTCHA displayed after max failed attempts.')

if __name__ == "__main__":
    unittest.main()
