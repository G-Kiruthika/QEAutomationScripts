
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