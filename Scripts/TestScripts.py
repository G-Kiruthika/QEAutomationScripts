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
        self.login_page.go_to_login_page()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        assert self.login_page.is_dashboard_displayed(), 'Dashboard was not displayed after valid login.'

    def test_TC_LOGIN_002(self):
        self.login_page.go_to_login_page()
        self.login_page.enter_email('wronguser@example.com')
        self.login_page.enter_password('WrongPass456!')
        self.login_page.click_login()
        assert self.login_page.is_error_message_displayed(), 'Error message was not displayed for invalid credentials.'

    def test_TC_LOGIN_003(self):
        self.login_page.test_login_with_empty_email('ValidPass123!')

    def test_TC_LOGIN_01(self):
        self.login_page.test_successful_login('user@example.com', 'ValidPassword123!')

    def test_TC_LOGIN_004(self):
        self.login_page.go_to_login_page()
        self.login_page.enter_email('user@example.com')
        self.login_page.clear_password()
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert 'password is required' in error_message.lower(), f'Expected error for empty password, got: {error_message}'

    def test_TC_LOGIN_02(self):
        self.login_page.go_to_login_page()
        self.login_page.enter_email('invaliduser@example.com')
        self.login_page.enter_password('ValidPassword123!')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert 'error' in error_message.lower() or 'login failed' in error_message.lower(), f'Expected error for invalid email, got: {error_message}'

    def test_TC_LOGIN_005(self):
        """
        Test Case TC_LOGIN_005: Login with empty fields validation.
        Steps:
        1. Navigate to the login page.
        2. Leave both email and password fields empty.
        3. Click the login button.
        4. Validate error messages for required fields.
        """
        self.login_page.login_with_empty_fields_and_validate_errors()

    def test_TC_LOGIN_03(self):
        """
        Test Case TC-LOGIN-03: Login with valid email and invalid password.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid registered email address (user@example.com).
        3. Enter an invalid password (WrongPassword).
        4. Click the login button.
        5. Validate login failure and error message.
        """
        self.login_page.login_with_valid_email_and_invalid_password('user@example.com', 'WrongPassword')
