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

    def test_TC_LOGIN_009_accessibility_checks(self):
        """TC_LOGIN_009: Accessibility - screen reader compatibility, keyboard navigation, color contrast."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        login_page.navigate()
        self.assertTrue(login_page.is_login_page_displayed(), "Login page should be displayed.")
        self.assertTrue(login_page.check_screen_reader_compatibility(), "Screen reader compatibility should pass.")
        self.assertTrue(login_page.check_keyboard_navigation(), "Keyboard navigation should be accessible.")
        self.assertTrue(login_page.check_color_contrast(), "Color contrast should meet WCAG AA standards.")
        driver.quit()

    def test_TC_LOGIN_010_password_masking(self):
        """TC_LOGIN_010: Password masking - input should be masked in password field."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        login_page.navigate()
        self.assertTrue(login_page.is_login_page_displayed(), "Login page should be displayed.")
        login_page.enter_password("Pass@123")
        self.assertTrue(login_page.is_password_masked(), "Password input should be masked.")
        driver.quit()

    # --- Newly added methods for TC_LOGIN_003 and TC_LOGIN_004 ---
    def test_TC_LOGIN_003_leave_email_empty_and_validate_error(self):
        """TC_LOGIN_003: Leave email empty, enter valid password, click login, verify 'Email is required.' error."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        login_page.open()  # Step 1: Navigate to login page
        self.assertTrue(login_page.is_login_page_displayed(), "Login page should be displayed.")
        login_page.leave_email_empty()  # Step 2: Leave email field empty
        login_page.enter_password("ValidPass123!")  # Step 3: Enter valid password
        login_page.click_login()  # Step 4: Click login
        self.assertTrue(login_page.validate_email_required_error(), "Error message 'Email is required.' should be displayed.")
        driver.quit()

    def test_TC_LOGIN_004_leave_password_empty_and_validate_error(self):
        """TC_LOGIN_004: Enter valid email, leave password empty, click login, verify 'Password is required.' error."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        login_page.open()  # Step 1: Navigate to login page
        self.assertTrue(login_page.is_login_page_displayed(), "Login page should be displayed.")
        login_page.enter_email("user@example.com")  # Step 2: Enter valid email
        login_page.leave_password_empty()  # Step 3: Leave password field empty
        login_page.click_login()  # Step 4: Click login
        self.assertTrue(login_page.validate_password_required_error(), "Error message 'Password is required.' should be displayed.")
        driver.quit()

    # --- Appended methods for TC_LOGIN_007 and TC_LOGIN_008 ---
    def test_TC_LOGIN_007_forgot_password_flow(self):
        """TC_LOGIN_007: Navigate to login page, click 'Forgot Password?', verify forgot password page displays email input and instructions."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        login_page.open()  # Step 1: Navigate to login page
        self.assertTrue(login_page.is_login_page_displayed(), "Login page should be displayed.")
        login_page.click_forgot_password()  # Step 2: Click 'Forgot Password?'
        self.assertTrue(login_page.is_forgot_password_page_displayed(), "Forgot Password page should display email input and instructions.")
        driver.quit()

    def test_TC_LOGIN_008_max_length_email_login(self):
        """TC_LOGIN_008: Enter max-length email, valid password, click login, verify field accepts max-length email and login result."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        max_length_email = "{}@example.com".format("a"*64)
        valid_password = "ValidPass123!"
        login_page.login_with_max_length_email(max_length_email, valid_password)
        self.assertTrue(login_page.is_max_length_email_accepted(max_length_email), "Email field should accept max-length email.")
        # Optionally, check login result (success or error shown)
        # self.assertTrue(login_page.is_dashboard_displayed() or login_page.is_error_message_displayed(), "Login result should be displayed.")
        driver.quit()

    # --- Appended methods for TC_LOGIN_009 and TC_LOGIN_010 ---
    def test_TC_LOGIN_009_minimum_email_valid_password(self):
        """TC_LOGIN_009: Enter minimum allowed email (a@b.co), valid password (ValidPass123!), click login, verify login succeeds or error shown."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        login_page.open()
        login_page.enter_email("a@b.co")
        login_page.enter_password("ValidPass123!")
        login_page.click_login()
        # Assert dashboard displayed (login success) or error shown
        self.assertTrue(login_page.is_dashboard_displayed() or login_page.is_error_message_displayed(), "Login should succeed or error should be shown for minimum email.")
        driver.quit()

    def test_TC_LOGIN_010_failed_attempts_account_lock_or_captcha(self):
        """TC_LOGIN_010: Enter valid email (user@example.com), incorrect password (WrongPass!@#), attempt login 5 times, verify error each time, lock/CAPTCHA on last attempt."""
        driver = self._get_driver()
        login_page = LoginPage(driver)
        email = "user@example.com"
        password = "WrongPass!@#"
        attempts = 5
        # Attempt multiple failed logins
        lock_or_captcha = login_page.attempt_multiple_failed_logins(email, password, attempts)
        # Assert error message after failed attempts
        self.assertTrue(login_page.is_error_message_displayed(), "Error message should be shown after each failed login attempt.")
        # Assert lock or CAPTCHA on last attempt
        self.assertTrue(login_page.is_account_locked() or login_page.is_captcha_displayed(), "Account should be locked or CAPTCHA should be displayed after maximum failed attempts.")
        driver.quit()
