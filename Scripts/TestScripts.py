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
        3. Enter a valid password: validPassword123
        4. Click the login button.
        5. Verify that the dashboard is displayed.
        """
        result = self.login_page.perform_login('user@example.com', 'validPassword123')
        assert result, "Login was not successful, dashboard not displayed."

    def test_TC_LOGIN_002_invalid(self):
        """
        Test Case TC_LOGIN_002: Login attempt with invalid credentials and error validation.
        Steps:
        1. Navigate to the login page.
        2. Enter an invalid email address: wronguser@example.com
        3. Enter an invalid password: wrongPassword
        4. Click the login button.
        5. Verify that an error message is displayed indicating invalid credentials.
        """
        result = self.login_page.perform_invalid_login('wronguser@example.com', 'wrongPassword')
        assert result, "Error message not displayed for invalid credentials."

    def test_TC_LOGIN_001_valid(self):
        """
        Test Case TC_LOGIN_001: Successful login with valid credentials.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid email address: user@example.com
        3. Enter a valid password: validPassword123
        4. Click the login button.
        5. Verify that the dashboard is displayed.
        """
        result = self.login_page.perform_login('user@example.com', 'validPassword123')
        assert result, "Login was not successful, dashboard not displayed."

    def test_TC_LOGIN_002_invalid(self):
        """
        Test Case TC_LOGIN_002: Login attempt with invalid credentials and error validation.
        Steps:
        1. Navigate to the login page.
        2. Enter an invalid email address: wronguser@example.com
        3. Enter an invalid password: wrongPassword
        4. Click the login button.
        5. Verify that an error message is displayed indicating invalid credentials.
        """
        result = self.login_page.perform_invalid_login('wronguser@example.com', 'wrongPassword')
        assert result, "Error message not displayed for invalid credentials."

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Attempt login with empty email and valid password.
        Steps:
        1. Navigate to the login page.
        2. Leave the email field empty.
        3. Enter a valid password: validPassword123
        4. Click the login button.
        5. Verify error message is displayed: 'Email/Username is required.'
        """
        result = self.login_page.login_with_empty_email('validPassword123')
        assert result, "Error message 'Email/Username is required.' was not displayed."

    def test_TC_LOGIN_004(self):
        """
        Test Case TC_LOGIN_004: Attempt login with valid email and empty password.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid email: user@example.com
        3. Leave the password field empty.
        4. Click the login button.
        5. Verify error message is displayed: 'Password is required.'
        """
        result = self.login_page.login_with_empty_password('user@example.com')
        assert result, "Error message 'Password is required.' was not displayed."

    # --- Appended for TC_LOGIN_005 ---
    def test_TC_LOGIN_005(self):
        """
        Test Case TC_LOGIN_005: Attempt login with both fields empty and verify error messages.
        Steps:
        1. Navigate to login page.
        2. Leave both email/username and password fields empty.
        3. Click the 'Login' button.
        4. Verify error messages: 'Email/Username is required.' and 'Password is required.'
        """
        result = self.login_page.perform_login_with_empty_fields()
        assert result, "Error messages 'Email/Username is required.' and 'Password is required.' were not displayed."

    # --- Appended for TC_LOGIN_006 ---
    def test_TC_LOGIN_006(self):
        """
        Test Case TC_LOGIN_006: Login with Remember Me and session persistence.
        Steps:
        1. Navigate to login page.
        2. Enter valid email/username and password.
        3. Select 'Remember Me' checkbox.
        4. Click the 'Login' button.
        5. Restart browser and revisit the site.
        6. Verify user remains logged in.
        """
        email = 'user@example.com'
        password = 'validPassword123'
        result = self.login_page.perform_login_with_remember_me(email, password)
        # Simulate browser restart and session persistence check
        session_persistent = self.login_page.verify_session_persistence()
        assert result and session_persistent, "User did not remain logged in after browser restart."
