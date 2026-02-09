import unittest
from Pages.LoginPage import LoginPage

class TestScripts(unittest.TestCase):
    def setUp(self):
        # You must provide a Selenium WebDriver instance here
        # For demonstration, this is a placeholder
        self.driver = None  # Replace with actual WebDriver instance
        self.login_page = LoginPage(self.driver)

    # TC_LOGIN_001: Valid login scenario
    def test_TC_LOGIN_001_valid_login(self):
        """
        Test Case TC_LOGIN_001: Valid login
        Steps:
        1. Navigate to the login page.
        2. Enter a valid registered email address in the email field.
        3. Enter a valid password in the password field.
        4. Click the 'Login' button.
        Expected: User is logged in and redirected to the account/dashboard page.
        """
        self.login_page.open()
        self.login_page.enter_email("user@example.com")
        self.login_page.enter_password("ValidPass123!")
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_dashboard_displayed(), "Dashboard should be displayed after successful login.")

    # TC_LOGIN_002: Invalid login scenario
    def test_TC_LOGIN_002_invalid_login(self):
        """
        Test Case TC_LOGIN_002: Invalid login
        Steps:
        1. Navigate to the login page.
        2. Enter an unregistered email address in the email field.
        3. Enter an incorrect password in the password field.
        4. Click the 'Login' button.
        Expected: Error message is displayed: 'Invalid email or password.' User is not logged in.
        """
        self.login_page.open()
        self.login_page.enter_email("invaliduser@example.com")
        self.login_page.enter_password("WrongPass!@#")
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_error_message_displayed("Invalid email or password."), "Error message 'Invalid email or password.' should be displayed.")

if __name__ == "__main__":
    unittest.main()
