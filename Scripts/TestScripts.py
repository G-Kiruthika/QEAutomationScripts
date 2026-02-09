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

    # TC_LOGIN_003: Empty email, valid password scenario
    def test_TC_LOGIN_003_empty_email_valid_password(self):
        """
        Test Case TC_LOGIN_003: Leave email empty, enter valid password, click login, expect 'Email is required.' error.
        Steps:
        1. Navigate to the login page.
        2. Leave the email field empty.
        3. Enter a valid password in the password field.
        4. Click the 'Login' button.
        Expected: Error message is displayed: 'Email is required.' User is not logged in.
        """
        password = "ValidPass123!"
        self.login_page.assert_email_required(password)

    # TC_LOGIN_004: Valid email, empty password scenario
    def test_TC_LOGIN_004_valid_email_empty_password(self):
        """
        Test Case TC_LOGIN_004: Enter valid email, leave password empty, click login, expect 'Password is required.' error.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid email address in the email field.
        3. Leave the password field empty.
        4. Click the 'Login' button.
        Expected: Error message is displayed: 'Password is required.' User is not logged in.
        """
        email = "user@example.com"
        self.login_page.assert_password_required(email)

if __name__ == "__main__":
    unittest.main()
