# Import necessary modules
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate_to_login_page()
        await self.login_page.enter_invalid_credentials('', '')
        assert self.login_page.is_error_message_displayed('Mandatory fields are required')

    async def test_remember_me_functionality(self):
        await self.login_page.navigate_to_login_page()
        # Implementation for remember me functionality goes here

    def test_invalid_login_credentials(self):
        """
        TC_LOGIN_001: Test invalid login and verify error message
        Steps:
        1. Navigate to login screen
        2. Enter invalid username and/or password
        3. Verify error message 'Invalid username or password. Please try again.' is displayed
        """
        self.login_page.navigate_to_login_page()
        self.login_page.enter_invalid_credentials('invaliduser@example.com', 'wrongpassword')
        assert self.login_page.is_error_message_displayed('Invalid username or password. Please try again.')
