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

    def test_TC_LOGIN_001_invalid_login_error(self):
        """
        TC_LOGIN_001: Navigate to login screen, enter invalid credentials, verify error message.
        Steps:
        1. Navigate to the login screen.
        2. Enter invalid username and/or password.
        3. Verify error message 'Invalid username or password. Please try again.' is displayed.
        Traceability: Uses LoginPage.go_to_login_page(), enter_invalid_credentials_and_submit(), verify_error_message_for_invalid_login()
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_invalid_credentials_and_submit('invalid_user', 'invalid_pass')
        assert self.login_page.verify_error_message_for_invalid_login(), (
            "Expected error message 'Invalid username or password. Please try again.' was not displayed after invalid login attempt."
        )
