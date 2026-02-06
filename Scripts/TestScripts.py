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
        self.login_page.go_to_login_page()
        self.login_page.login_with_invalid_credentials(username, password)
        result = self.login_page.verify_invalid_login_error(expected_error)
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

    def test_TC_LOGIN_001_pageclass(self):
        """
        TC_LOGIN_001: Navigate to login, enter invalid credentials, submit, and verify error message using PageClass methods.
        Steps:
        1. Navigate to the login page.
        2. Enter invalid credentials and submit.
        3. Verify the error message is as expected.
        """
        username = 'invalid_user'
        password = 'invalid_pass'
        expected_error = 'Invalid username or password. Please try again.'
        self.login_page.go_to_login_page()
        self.login_page.login_with_invalid_credentials(username, password)
        result = self.login_page.verify_invalid_login_error(expected_error)
        assert result, f"Expected error message '{expected_error}', but got something else."
