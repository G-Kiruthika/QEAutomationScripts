import unittest
from PageClasses.LoginPage import LoginPage
from PageClasses.ProfilePage import ProfilePage
from PageClasses.SettingsPage import SettingsPage

class TestScripts(unittest.TestCase):

    def setUp(self):
        self.login_page = LoginPage()
        self.profile_page = ProfilePage()
        self.settings_page = SettingsPage()

    # Existing test methods...

    # TC_LOGIN_009: Minimum allowed email length, valid password, login, validation of login or error
    def test_TC_LOGIN_009_min_email_length_valid_password(self):
        """Test login with minimum allowed email length and valid password"""
        min_email = "a@b.co"  # Assuming this is the minimum allowed email length
        valid_password = "ValidPass123!"

        self.login_page.open_login_page()
        self.login_page.login_with_credentials(min_email, valid_password)

        if self.login_page.is_login_successful():
            # Validate that user is redirected to profile page or dashboard
            self.assertTrue(self.profile_page.is_profile_page_displayed(), "Profile page should be displayed after successful login.")
        else:
            # Validate error message for invalid email
            error_msg = self.login_page.get_error_message()
            self.assertIn("Invalid email", error_msg, "Error message for minimum email length should mention invalid email.")

    # TC_LOGIN_010: Valid email, incorrect password, repeated login attempts, error message for each, account lock/CAPTCHA on final attempt
    def test_TC_LOGIN_010_valid_email_incorrect_password_multiple_attempts(self):
        """Test login with valid email and incorrect password, multiple attempts, expect account lock or CAPTCHA"""
        valid_email = "user@example.com"
        incorrect_password = "WrongPass!"
        max_attempts = 5  # Assuming account lock/CAPTCHA triggers after 5 failed attempts

        self.login_page.open_login_page()
        for attempt in range(1, max_attempts + 1):
            self.login_page.login_with_credentials(valid_email, incorrect_password)
            error_msg = self.login_page.get_error_message()
            self.assertIn("Incorrect password", error_msg, f"Attempt {attempt}: Error message should mention incorrect password.")

        # After max_attempts, check for account lock or CAPTCHA
        locked_or_captcha = self.login_page.is_account_locked_or_captcha_displayed()
        self.assertTrue(locked_or_captcha, "Account should be locked or CAPTCHA should be displayed after multiple failed login attempts.")

    # TC_LOGIN_001: Valid login scenario
    def test_TC_LOGIN_001_valid_login(self):
        """Test login with valid credentials, expect dashboard display"""
        self.login_page.open()
        self.login_page.enter_email("user1")
        self.login_page.enter_password("Pass@123")
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_dashboard_displayed(), "Dashboard should be displayed after successful login.")

    # TC_LOGIN_002: Invalid login scenario
    def test_TC_LOGIN_002_invalid_login(self):
        """Test login with invalid credentials, expect error message"""
        self.login_page.open()
        self.login_page.enter_email("invalidUser")
        self.login_page.enter_password("WrongPass")
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_error_message_displayed("Invalid credentials"), "Error message for invalid credentials should be displayed.")

if __name__ == "__main__":
    unittest.main()
