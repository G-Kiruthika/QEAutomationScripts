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
        self.login_page.go_to_login_page()
        invalid_email = "invalid@example.com"
        invalid_password = "wrongpassword"
        self.login_page.login_with_credentials(invalid_email, invalid_password)
        assert self.login_page.is_error_message_displayed("Invalid username or password. Please try again."), "Error message not displayed as expected."

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
        2. Click 'Forgot Username' link.
        3. Enter email for username recovery.
        4. Submit the recovery form.
        5. Assert recovery is successful and username is retrieved.
        """
        self.login_page.go_to_login_page()
        self.login_page.click_forgot_username_link()
        test_email = "user@example.com"
        self.login_page.enter_email_for_username_recovery(test_email)
        self.login_page.submit_username_recovery()
        assert self.login_page.is_username_recovery_successful(), "Username recovery was not successful."
        recovered_username = self.login_page.get_recovered_username()
        assert recovered_username != "", "Recovered username should not be empty."
