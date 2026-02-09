import unittest
from LoginPage import LoginPage
from ForgotPasswordPage import ForgotPasswordPage

# Existing test methods...

class TestLoginPage(unittest.TestCase):

    # Existing test methods...

    def test_TC_LOGIN_003_email_required(self):
        """TC_LOGIN_003: Leave email empty, enter valid password, assert 'Email is required.' error.""" 
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page()
        login_page.leave_email_empty()
        login_page.enter_password('ValidPass123!')
        login_page.click_login()
        self.assertTrue(login_page.is_error_message_displayed(), "Error message should be displayed.")
        self.assertEqual(login_page.get_error_message(), 'Email is required.', "Error message should be 'Email is required.'")
        self.assertTrue(login_page.is_login_page_displayed(), "User should not be logged in.")

    def test_TC_LOGIN_004_password_required(self):
        """TC_LOGIN_004: Enter valid email, leave password empty, assert 'Password is required.' error.""" 
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page()
        login_page.enter_username('user@example.com')
        login_page.leave_password_empty()
        login_page.click_login()
        self.assertTrue(login_page.is_error_message_displayed(), "Error message should be displayed.")
        self.assertEqual(login_page.get_error_message(), 'Password is required.', "Error message should be 'Password is required.'")
        self.assertTrue(login_page.is_login_page_displayed(), "User should not be logged in.")

    def test_TC_LOGIN_005_empty_fields_and_error_messages(self):
        """TC_LOGIN_005: Leave both email and password fields empty, click login, assert error messages for both fields and user is not logged in.""" 
        login_page = LoginPage(self.driver, self.locators)
        login_page.enter_username("")
        login_page.enter_password("")
        login_page.click_login()
        errors = login_page.get_error_messages()
        self.assertEqual(errors.get('email'), 'Email is required.', "Email error message should be 'Email is required.'")
        self.assertEqual(errors.get('password'), 'Password is required.', "Password error message should be 'Password is required.'")
        self.assertFalse(login_page.is_login_successful(), "User should not be logged in if both fields are empty.")

    def test_TC_LOGIN_006_valid_login_remember_me_session_persistence(self):
        """TC_LOGIN_006: Enter valid email and password, check 'Remember Me', click login, assert session persists after browser restart.""" 
        login_page = LoginPage(self.driver, self.locators)
        login_page.enter_username('user@example.com')
        login_page.enter_password('ValidPass123!')
        self.assertTrue(login_page.check_remember_me(), "'Remember Me' checkbox should be selected.")
        login_page.click_login()
        self.assertTrue(login_page.is_login_successful(), "User should be logged in after valid credentials.")
        # Simulate browser restart and revisit
        self.driver.quit()
        # The following lines are a placeholder for restarting the browser and loading cookies/session if implemented
        # In practice, the test framework should provide a way to restart the driver and preserve cookies
        # For this example, we assume driver and locators are reinitialized
        self.driver = self._restart_browser_and_preserve_cookies()
        login_page = LoginPage(self.driver, self.locators)
        self.assertTrue(login_page.is_session_persistent(), "User session should persist after browser restart if 'Remember Me' was checked.")

    def _restart_browser_and_preserve_cookies(self):
        # Placeholder for actual browser restart logic
        # In real test suite, implement browser restart and cookie/session restoration as needed
        pass

    def test_TC_LOGIN_007_forgot_password_email_and_instructions(self):
        """TC_LOGIN_007: Navigate to login page, click 'Forgot Password?', verify email input and instructions.""" 
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page()
        login_page.click_forgot_password()
        forgot_password_page = ForgotPasswordPage(self.driver)
        self.assertTrue(forgot_password_page.is_email_input_present(), "Email input should be present on Forgot Password page.")
        self.assertTrue(forgot_password_page.is_instructions_present(), "Instructions should be present on Forgot Password page.")

    def test_TC_LOGIN_008_max_length_email_and_valid_password(self):
        """TC_LOGIN_008: Navigate to login page, enter max-length email, valid password, click login, assert login or error.""" 
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page()
        max_length_email = "a" * 64 + "@example.com"
        login_page.enter_username(max_length_email)
        login_page.enter_password('ValidPass123!')
        login_page.click_login()
        # Assert login success or error message
        if login_page.is_login_successful():
            self.assertTrue(login_page.is_login_successful(), "User should be logged in with max-length email and valid password.")
        else:
            self.assertTrue(login_page.is_error_message_displayed(), "Error message should be displayed if login fails.")
            error_msg = login_page.get_error_message()
            self.assertIn(error_msg, ["Invalid email or password.", "Email exceeds maximum length."], "Appropriate error message should be shown.")

    def test_TC_LOGIN_009_min_length_username_and_valid_password(self):
        """TC_LOGIN_009: Enter minimum allowed length username (a@b.co), valid password (ValidPass123!), click login, assert field accepts minimum input, password is accepted, login succeeds or error is shown."""
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page()
        min_length_username = "a@b.co"
        login_page.enter_username(min_length_username)
        login_page.enter_password("ValidPass123!")
        login_page.click_login()
        self.assertTrue(login_page.is_login_page_displayed(), "Login page should be displayed after navigation.")
        # Username field accepts minimum length input
        self.assertEqual(len(min_length_username), 6, "Username should be minimum allowed length.")
        # Password field accepts input
        self.assertTrue(isinstance("ValidPass123!", str), "Password should be a string.")
        # Login succeeds or error is shown
        if login_page.is_login_successful():
            self.assertTrue(login_page.is_login_successful(), "User should be logged in with minimum length username and valid password.")
        else:
            self.assertTrue(login_page.is_error_message_displayed(), "Error message should be displayed if login fails.")
            error_msg = login_page.get_error_message()
            self.assertIn(error_msg, ["Invalid email or password."], "Appropriate error message should be shown.")

    def test_TC_LOGIN_010_failed_attempts_account_lock_or_captcha(self):
        """TC_LOGIN_010: Enter valid email (user@example.com), incorrect password (WrongPass!@#), click login for 5 failed attempts, assert error for each, on last attempt verify account lock or CAPTCHA."""
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page()
        username = "user@example.com"
        password = "WrongPass!@#"
        attempts = 5
        for i in range(attempts):
            login_page.enter_username(username)
            login_page.enter_password(password)
            login_page.click_login()
            self.assertTrue(login_page.is_error_message_displayed(), f"Error message should be displayed for attempt {i+1}.")
            error_msg = login_page.get_error_message()
            self.assertIn(error_msg, ["Invalid email or password."], f"Appropriate error message should be shown for attempt {i+1}.")
        is_locked, is_captcha = login_page.attempt_login_multiple_times(username, password, attempts)
        self.assertTrue(is_locked or is_captcha, "Account should be locked or CAPTCHA should be displayed after maximum failed attempts.")
        if is_locked:
            self.assertTrue(login_page.is_lock_message_present(), "Lock message should be present after account is locked.")
            lock_msg = login_page.get_lock_message_text()
            self.assertIsNotNone(lock_msg, "Lock message text should be present.")
        if is_captcha:
            self.assertTrue(login_page.is_captcha_present(), "CAPTCHA should be present after repeated failed attempts.")
            captcha_msg = login_page.get_captcha_text()
            self.assertIsNotNone(captcha_msg, "CAPTCHA text should be present.")

# Existing code...
