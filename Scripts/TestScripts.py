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

    def test_TC_LOGIN_005_empty_fields_error_messages(self):
        """TC_LOGIN_005: Leave both email and password fields empty, click login, assert error messages for both fields and verify user not logged in."""
        login_page = LoginPage(self.driver, self.locators)
        login_page.navigate_to_login_page('https://example.com/login')
        login_page.leave_fields_empty_and_login()
        email_error, password_error = login_page.get_error_messages()
        self.assertEqual(email_error, 'Email is required.', "Email error message should be 'Email is required.'")
        self.assertEqual(password_error, 'Password is required.', "Password error message should be 'Password is required.'")
        self.assertFalse(login_page.is_login_successful(), "User should not be logged in.")

    def test_TC_LOGIN_006_remember_me_and_session_persistence(self):
        """TC_LOGIN_006: Enter valid email and password, check 'Remember Me', login, assert user logged in, close/reopen browser, revisit site, assert session persists."""
        login_page = LoginPage(self.driver, self.locators)
        login_page.navigate_to_login_page('https://example.com/login')
        login_page.login_with_credentials('user@example.com', 'ValidPass123!', remember_me=True)
        self.assertTrue(login_page.is_login_successful(), "User should be logged in.")
        session_persists = login_page.verify_session_persistence('https://example.com/login')
        self.assertTrue(session_persists, "Session should persist after browser restart.")

# Existing code...
