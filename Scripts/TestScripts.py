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

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Empty Fields Validation
        Steps:
        1. Navigate to the login page.
        2. Leave username and/or password fields empty.
        3. Click the Login button.
        4. Verify error message prompting to fill in required fields.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_credentials(username="", password="")
        self.login_page.click_login()
        error_message = self.login_page.assert_empty_field_prompt()
        assert error_message is not None and 'Mandatory fields are required' in error_message, f"Expected prompt for mandatory fields, got: {error_message}"

    def test_TC_LOGIN_004(self):
        """
        Test Case TC_LOGIN_004: Remember Me Functionality and Login Persistence
        Steps:
        1. Navigate to the login page.
        2. Enter valid credentials and check 'Remember Me'.
        3. Click the Login button.
        4. Close and reopen the browser, navigate to the site.
        5. Verify user remains logged in.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_credentials(username="user1", password="Pass@123")
        self.login_page.check_remember_me()
        self.login_page.click_login()
        assert self.login_page.is_logged_in(), "User should be logged in after valid credentials."
        self.login_page.close_and_reopen_browser()
        self.login_page.go_to_login_page()
        assert self.login_page.is_logged_in(), "User should remain logged in after browser restart with 'Remember Me' checked."
