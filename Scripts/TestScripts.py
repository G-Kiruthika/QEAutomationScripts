
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

# Existing code...
