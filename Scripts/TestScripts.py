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
        Test Case TC-LOGIN-002: Navigate to login screen and verify 'Remember Me' checkbox is absent.
        Steps:
        1. Navigate to the login screen.
        2. Assert that 'Remember Me' checkbox is not present.
        """
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_absent()

    def test_TC_LOGIN_002_invalid_email(self):
        """
        Test Case TC-LOGIN-002 (Invalid Email):
        Steps:
        1. Navigate to the login page
        2. Enter invalid/non-existent email (invalid@example.com)
        3. Enter valid password (ValidPass123!)
        4. Click the Login button
        5. Assert error message 'Invalid email or password' is displayed
        6. Verify user remains on login page
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('invalid@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        assert self.login_page.get_error_message() == 'Invalid email or password', "Error message 'Invalid email or password' was not displayed."
        assert self.login_page.is_on_login_page(), "User did not remain on the login page after invalid login attempt."

    def test_TC_LOGIN_003(self):
        """
        Test Case TC-LOGIN-003: Valid email, invalid password, verify error and page state
        Steps:
        1. Navigate to the login page (URL: https://ecommerce.example.com/login)
        2. Enter valid registered email address (testuser@example.com)
        3. Enter incorrect password (WrongPassword123)
        4. Click the Login button
        5. Assert error message 'Invalid email or password' is displayed
        6. Verify user remains on login page
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('testuser@example.com')
        self.login_page.enter_password('WrongPassword123')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message == 'Invalid email or password', f"Expected error message 'Invalid email or password', but got '{error_message}'."
        assert self.login_page.is_on_login_page(), "User did not remain on the login page after invalid login attempt."

    def test_TC_LOGIN_005(self):
        """
        Test Case TC-LOGIN-005: Valid email, empty password, verify validation error and that login is not processed
        Steps:
        1. Navigate to the login page (URL: https://ecommerce.example.com/login)
        2. Enter valid registered email address (testuser@example.com)
        3. Leave the password field empty
        4. Click the Login button
        5. Assert validation error is displayed for empty password
        6. Verify login is not processed (user remains on login page, no authentication)
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('testuser@example.com')
        self.login_page.enter_password('')
        self.login_page.click_login()
        # Check for validation error in one of the possible ways
        error_message = self.login_page.get_error_message()
        validation_error = self.login_page.get_validation_error()
        empty_prompt = self.login_page.is_empty_field_prompt_visible()
        assert (
            ('password' in error_message.lower() and error_message.strip() != '') or
            ('password' in validation_error.lower() and validation_error.strip() != '') or
            empty_prompt
        ), (
            f"Expected password validation error or prompt, but got: error_message='{error_message}', validation_error='{validation_error}', empty_prompt={empty_prompt}"
        )
        self.login_page.assert_login_not_processed()
