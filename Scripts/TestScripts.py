# Import necessary modules
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

    def test_TC_LOGIN_001(self):
        """Test invalid login and error message for TC_LOGIN_001"""
        username = 'invalid_user'
        password = 'invalid_pass'
        expected_error = 'Invalid username or password. Please try again.'
        result = self.login_page.login_with_invalid_credentials_and_verify_error(username, password, expected_error)
        assert result, f"Expected error message '{expected_error}', but got something else."

    def test_TC_LOGIN_002(self):
        """
        Test Case TC_LOGIN_002: Navigate to login screen and verify 'Remember Me' checkbox is absent.
        Steps:
        1. Navigate to the login screen.
        2. Assert that 'Remember Me' checkbox is not present.
        """
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_absent()

    def test_TC_LOGIN_001_valid_login(self):
        """
        Test Case TC_LOGIN_001: Valid login flow
        Steps:
        1. Navigate to login page.
        2. Enter valid email.
        3. Enter valid password.
        4. Click login.
        5. Verify dashboard is displayed.
        """
        email = 'user@example.com'
        password = 'ValidPass123!'
        result = self.login_page.login_valid_user(email, password)
        assert result, "Dashboard was not displayed after valid login."

    def test_TC_LOGIN_002_invalid_login(self):
        """
        Test Case TC_LOGIN_002: Invalid login flow
        Steps:
        1. Navigate to login page.
        2. Enter invalid email.
        3. Enter invalid password.
        4. Click login.
        5. Verify error message is displayed.
        """
        email = 'wronguser@example.com'
        password = 'WrongPass456!'
        error_message = self.login_page.login_invalid_user(email, password)
        assert error_message is not None and 'invalid credentials' in error_message.lower(), f"Expected error message for invalid credentials, got: {error_message}"
