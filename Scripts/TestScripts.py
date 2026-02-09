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
        2. Enter valid username and password (user1 / Pass@123).
        3. Click the Login button.
        4. Verify dashboard is present.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.click_login()
        assert self.login_page.verify_dashboard_present(), 'Dashboard not present after valid login.'

    def test_TC_LOGIN_002_invalid(self):
        """
        Test Case TC_LOGIN_002: Invalid login and error message verification
        Steps:
        1. Navigate to the login page.
        2. Enter invalid username and password (invalidUser / WrongPass).
        3. Click the Login button.
        4. Verify error message is present.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('invalidUser')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login()
        assert self.login_page.verify_error_message_present(), 'Error message not present after invalid login.'
