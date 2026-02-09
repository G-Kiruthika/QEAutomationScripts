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
        TC_LOGIN_001: Valid login with username 'user1' and password 'Pass@123', expect dashboard displayed.
        Steps:
        1. Navigate to login page.
        2. Enter valid username and password.
        3. Click login.
        4. Assert dashboard is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.click_login()
        assert self.login_page.is_dashboard_displayed(), "Dashboard should be displayed after valid login."

    def test_TC_LOGIN_002_invalid_login(self):
        """
        TC_LOGIN_002: Invalid login with username 'invalidUser' and password 'WrongPass', expect error message displayed.
        Steps:
        1. Navigate to login page.
        2. Enter invalid username and password.
        3. Click login.
        4. Assert error message is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('invalidUser')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login()
        assert self.login_page.is_error_message_displayed(), "Error message should be displayed for invalid login."
