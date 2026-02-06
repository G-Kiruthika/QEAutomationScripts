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
        """
        TC_LOGIN_001: Invalid login and error message
        Steps:
        1. Navigate to the login screen
        2. Enter invalid username/password
        3. Submit login
        4. Verify error message
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('invalid_user@example.com')
        self.login_page.enter_password('invalid_pass')
        self.login_page.submit_login()
        self.login_page.assert_error_message('Invalid username or password. Please try again.')

    def test_TC_LOGIN_002(self):
        """
        TC_LOGIN_002: Navigate to login screen and verify 'Remember Me' checkbox is absent.
        """
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_absent()
