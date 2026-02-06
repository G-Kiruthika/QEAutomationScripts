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
        """
        Test Case TC_LOGIN_001: Invalid login should show error message
        Steps:
        1. Navigate to the login screen.
        2. Enter invalid username and password.
        3. Submit the login form.
        4. Assert the error message is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_credentials('invalid_user', 'invalid_pass')
        self.login_page.submit_login()
        self.login_page.assert_invalid_login_error('Invalid username or password. Please try again.')

    def test_TC_LOGIN_002(self):
        """
        Test Case TC_LOGIN_002: Navigate to login screen and verify 'Remember Me' checkbox is absent.
        Steps:
        1. Navigate to the login screen.
        2. Assert that 'Remember Me' checkbox is not present.
        """
        self.login_page.navigate_to_login()
        self.login_page.assert_remember_me_checkbox_absent()

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Forgot Username workflow
        Steps:
        1. Navigate to the login screen.
        2. Click on 'Forgot Username' link.
        3. Follow the instructions to recover username (provide sample email: 'user@example.com').
        4. Assert that the username is retrieved (success message appears).
        If not, retrieve and print error message.
        """
        forgot_username_page = ForgotUsernamePage(self.driver)
        forgot_username_page.navigate_to_login_page()
        forgot_username_page.click_forgot_username_link()
        forgot_username_page.enter_email('user@example.com')
        forgot_username_page.submit_recovery()
        if forgot_username_page.is_success_message_displayed():
            assert forgot_username_page.get_success_message() == 'Your username has been sent to your email address.'
        else:
            error_msg = forgot_username_page.get_error_message()
            print(f"Error retrieving username: {error_msg}")
            assert False, f"Failed to retrieve username: {error_msg}"
