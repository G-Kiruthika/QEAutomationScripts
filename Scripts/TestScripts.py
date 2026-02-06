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

    def test_TC_LOGIN_001_page_methods(self):
        """
        Appended method for TC_LOGIN_001 using PageClass atomic methods.
        Steps:
        1. Navigate to the login screen.
        2. Enter invalid credentials.
        3. Submit login.
        4. Verify error message.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_credentials('invalid_user', 'invalid_pass')
        self.login_page.submit_login()
        assert self.login_page.is_error_message_displayed('Invalid username or password. Please try again.'), "Error message not displayed as expected."

    def test_tc_login_001_atomic_methods(self):
        """
        Test Case TC_LOGIN_001 using only atomic PageClass methods.
        Steps:
        1. Navigate to the login screen.
        2. Enter invalid credentials.
        3. Submit login form.
        4. Verify error message.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_invalid_credentials('invalid_user', 'wrong_pass')
        self.login_page.submit_login_form()
        assert self.login_page.verify_error_message('Invalid username or password. Please try again.'), "Expected error message was not displayed."
