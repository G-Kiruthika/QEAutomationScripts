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
        """Test invalid login and error message for TC-LOGIN-001"""
        username = 'invalid_user'
        password = 'invalid_pass'
        expected_error = 'Invalid username or password. Please try again.'
        result = self.login_page.login_with_invalid_credentials_and_verify_error(username, password, expected_error)
        assert result, f"Expected error message '{expected_error}', but got something else."

    def test_TC_LOGIN_002(self):
        """
        Test Case TC-LOGIN-002: Navigate to login screen and verify 'Remember Me' checkbox is absent.
        Steps:
        1. Navigate to the login screen.
        2. Assert that 'Remember Me' checkbox is not present.
        """
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_absent()

    def test_TC_LOGIN_001_valid(self):
        """
        Test Case TC-LOGIN-001: Valid Login
        Steps:
        1. Navigate to the login page.
        2. Enter valid email (testuser@example.com) and password (ValidPass123!).
        3. Click Login.
        4. Verify dashboard header and user profile icon are visible.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('testuser@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        assert self.login_page.is_dashboard_header_visible(), 'Dashboard header not visible after login.'
        assert self.login_page.is_user_profile_icon_visible(), 'User profile icon not visible after login.'
