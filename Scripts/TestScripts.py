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
        Test Case TC_LOGIN_001: Valid login.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid email address (user@example.com).
        3. Enter a valid password (ValidPass123!).
        4. Click the login button.
        5. Verify user is redirected to the dashboard.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        assert self.login_page.is_dashboard_displayed(), 'Dashboard was not displayed after valid login.'

    def test_TC_LOGIN_002(self):
        """
        Test Case TC_LOGIN_002: Invalid login.
        Steps:
        1. Navigate to the login page.
        2. Enter an invalid email address (wronguser@example.com).
        3. Enter an invalid password (WrongPass456!).
        4. Click the login button.
        5. Verify error message for invalid credentials is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('wronguser@example.com')
        self.login_page.enter_password('WrongPass456!')
        self.login_page.click_login()
        assert self.login_page.is_error_message_displayed(), 'Error message was not displayed for invalid credentials.'

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Leave email empty, enter valid password, click login, verify error message.
        Steps:
        1. Navigate to the login page.
        2. Leave the email field empty.
        3. Enter a valid password (ValidPass123!).
        4. Click the login button.
        5. Verify error message is displayed indicating email is required.
        """
        self.login_page.go_to_login_page()
        self.login_page.login_with_empty_email('ValidPass123!')
        error_message = self.login_page.get_error_message()
        assert 'email is required' in error_message.lower(), f'Expected error message about email requirement, got: {error_message}'

    def test_TC_LOGIN_01(self):
        """
        Test Case TC-LOGIN-01: Enter valid email and password, click login, verify dashboard/homepage.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid registered email address (user@example.com).
        3. Enter the correct password for the email (ValidPassword123!).
        4. Click the 'Login' button.
        5. Verify user is successfully logged in and redirected to the dashboard/homepage.
        """
        self.login_page.go_to_login_page()
        self.login_page.login_with_valid_credentials('user@example.com', 'ValidPassword123!')
        assert self.login_page.is_user_on_dashboard(), 'User was not redirected to dashboard/homepage after login.'