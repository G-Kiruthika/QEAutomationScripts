# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.ForgotUsernamePage import ForgotUsernamePage

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
        Test Case TC_LOGIN_003: Forgot Username workflow
        Steps:
        1. Navigate to the login screen.
        2. Click on 'Forgot Username' link.
        3. Follow instructions to recover username.
        4. Retrieve and assert username is returned.
        """
        forgot_username_page = ForgotUsernamePage(self.driver)
        forgot_username_page.navigate_to_login()
        forgot_username_page.click_forgot_username_link()
        forgot_username_page.follow_instructions_and_recover_username('testuser@example.com')
        recovered_username = forgot_username_page.get_recovered_username()
        assert recovered_username is not None and recovered_username != "", "Username recovery failed or returned empty value."
