import unittest
from LoginPage import LoginPage

class TestLogin(unittest.TestCase):

    # ... Existing test methods remain unchanged ...

    def test_TC_LOGIN_007_multiple_failed_logins_account_lock_or_captcha(self):
        """TC_LOGIN_007: Attempt 10 failed logins with incorrect credentials and verify account lock or CAPTCHA is triggered and error message is displayed."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        username = "user1"
        password = "wrongPass"
        fail_count = 10
        result = login_page.attempt_multiple_failed_logins(username, password, fail_count)
        self.assertTrue(result['error_displayed'], "Error message should be displayed after failed login attempts.")
        self.assertTrue(result['lock_or_captcha_triggered'], "Account lock or CAPTCHA should be triggered after multiple failed logins.")
        driver.quit()

    def test_TC_LOGIN_008_multiple_valid_logins_response_time(self):
        """TC_LOGIN_008: Simulate 10 valid logins with correct credentials, measure response times, and ensure logins remain responsive."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        username = "user1"
        password = "Pass@123"
        login_count = 10
        max_allowed_response_time = 3.0  # seconds
        response_times = login_page.attempt_multiple_valid_logins(username, password, login_count)
        self.assertEqual(len(response_times), login_count, "Should record response time for each login attempt.")
        for i, resp_time in enumerate(response_times):
            self.assertLessEqual(resp_time, max_allowed_response_time, f"Login attempt {i+1} exceeded max allowed response time ({max_allowed_response_time}s).")
        driver.quit()

    # Utility method for driver setup (assumed present in existing TestScripts.py)
    def _get_driver(self):
        # ... driver initialization logic ...
        pass

    def test_TC_LOGIN_009_accessibility_check(self):
        """TC_LOGIN_009: Accessibility check - screen reader compatibility, keyboard navigation, and color contrast."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        accessibility = login_page.is_login_page_accessible()
        self.assertTrue(accessibility['screen_reader_compatible'], "Screen reader compatibility failed.")
        self.assertTrue(accessibility['keyboard_navigation'], "Keyboard navigation failed.")
        self.assertTrue(accessibility['color_contrast'], "Color contrast failed.")
        driver.quit()

    def test_TC_LOGIN_010_password_masking(self):
        """TC_LOGIN_010: Password masking - verify password input is masked."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.enter_password('Pass@123')
        self.assertTrue(login_page.is_password_masked(), "Password is not masked.")
        driver.quit()
