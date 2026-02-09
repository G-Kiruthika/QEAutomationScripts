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
        Test Case TC_LOGIN_001: Valid login and dashboard verification.
        Steps:
        1. Navigate to the login page.
        2. Enter valid username and password (user1/Pass@123).
        3. Click the Login button.
        4. Verify dashboard is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.click_login_button()
        assert self.login_page.is_dashboard_displayed(), "Dashboard should be displayed after valid login."

    def test_TC_LOGIN_002(self):
        """
        Test Case TC_LOGIN_002: Invalid login and error message verification.
        Steps:
        1. Navigate to the login page.
        2. Enter invalid username and password (invalidUser/WrongPass).
        3. Click the Login button.
        4. Verify error message is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('invalidUser')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login_button()
        assert self.login_page.is_error_message_displayed(), "Error message should be displayed for invalid login."
