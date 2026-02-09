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

    def test_TC_LOGIN_001_valid(self):
        """
        Test Case TC_LOGIN_001: Successful login with valid credentials.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid email address: user@example.com
        3. Enter a valid password: ValidPass123!
        4. Click the login button.
        5. Verify that the dashboard is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        self.login_page.verify_dashboard_displayed()

    def test_TC_LOGIN_002_invalid(self):
        """
        Test Case TC_LOGIN_002: Login attempt with invalid credentials and error validation.
        Steps:
        1. Navigate to the login page.
        2. Enter an invalid email address: wronguser@example.com
        3. Enter an invalid password: WrongPass456!
        4. Click the login button.
        5. Verify that an error message is displayed indicating invalid credentials.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('wronguser@example.com')
        self.login_page.enter_password('WrongPass456!')
        self.login_page.click_login()
        self.login_page.verify_error_message_displayed()
