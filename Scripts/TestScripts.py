import unittest
from LoginPage import LoginPage

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

# Existing code...
