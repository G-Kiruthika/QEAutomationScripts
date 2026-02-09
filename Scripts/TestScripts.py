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

    def test_TC_LOGIN_001_valid(self):
        """
        Test Case TC_LOGIN_001: Valid login and dashboard verification
        Steps:
        1. Navigate to the login page.
        2. Enter valid username 'user1' and password 'Pass@123'.
        3. Click Login.
        4. Verify dashboard is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.click_login()
        assert self.login_page.is_dashboard_header_displayed(), 'Dashboard header should be visible after successful login.'
        assert self.login_page.is_user_profile_icon_displayed(), 'User profile icon should be visible after successful login.'

    def test_TC_LOGIN_002_invalid(self):
        """
        Test Case TC_LOGIN_002: Invalid login and error message verification
        Steps:
        1. Navigate to the login page.
        2. Enter invalid username 'invalidUser' and password 'WrongPass'.
        3. Click Login.
        4. Verify error message for invalid credentials is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('invalidUser')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login()
        assert self.login_page.is_error_message_displayed(), 'Error message should be displayed for invalid credentials.'
        error_text = self.login_page.get_error_message_text()
        assert 'invalid' in error_text.lower(), f'Expected error message to mention invalid credentials, got: {error_text}'

    # --- TC_LOGIN_003 ---
    def test_TC_LOGIN_003_empty_fields_prompt(self):
        """
        Test Case TC_LOGIN_003: Validate error prompt for empty fields
        Steps:
        1. Navigate to the login page.
        2. Leave username and/or password fields empty.
        3. Click the Login button.
        4. Verify error message is displayed prompting to fill in required fields.
        """
        self.login_page.go_to_login_page()
        self.login_page.leave_fields_empty()
        self.login_page.click_login_button()
        error_prompt = self.login_page.get_empty_field_prompt()
        assert error_prompt == 'Mandatory fields are required', f'Expected "Mandatory fields are required", got: {error_prompt}'

    # --- TC_LOGIN_004 ---
    def test_TC_LOGIN_004_remember_me_auto_login(self):
        """
        Test Case TC_LOGIN_004: Validate Remember Me and auto-login
        Steps:
        1. Navigate to the login page.
        2. Enter valid credentials and check "Remember Me" option.
        3. Click the Login button.
        4. Close and reopen the browser, navigate to the site.
        5. Verify user remains logged in or is auto-logged in.
        """
        self.login_page.go_to_login_page()
        self.login_page.login('user1', 'Pass@123', remember_me=True)
        assert self.login_page.is_user_logged_in(), 'User should be logged in after valid credentials and Remember Me.'
        self.login_page.close_and_reopen_browser()
        self.login_page.go_to_login_page()
        assert self.login_page.is_user_logged_in(), 'User should remain logged in or be auto-logged in after browser restart.'
