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
        Test Case TC_LOGIN_001: Valid login flow.
        Steps:
        1. Navigate to the login page.
        2. Enter valid username and password.
        3. Click the Login button.
        4. Verify dashboard header is displayed.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.enter_email('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.click_login()
        assert self.login_page.verify_dashboard_header(), "Dashboard header not visible after login."

    def test_TC_LOGIN_002_invalid(self):
        """
        Test Case TC_LOGIN_002: Invalid login flow.
        Steps:
        1. Navigate to the login page.
        2. Enter invalid username and/or password.
        3. Click the Login button.
        4. Verify error message for invalid credentials.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.enter_email('invalidUser')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login()
        assert self.login_page.verify_error_message('Invalid username or password. Please try again.'), "Error message not displayed for invalid credentials."

    def test_TC_LOGIN_003_empty_fields_error(self):
        """
        Test Case TC_LOGIN_003: Submit empty login fields and verify error/validation message.
        Steps:
        1. Navigate to the login page.
        2. Leave username and password fields empty.
        3. Click the Login button.
        4. Verify error message prompting to fill in required fields.
        """
        self.login_page.login_with_empty_fields_and_verify_error()

    def test_TC_LOGIN_004_remember_me_auto_login(self):
        """
        Test Case TC_LOGIN_004: Login with 'Remember Me', close/reopen browser, verify auto-login.
        Steps:
        1. Navigate to the login page.
        2. Enter valid credentials and check 'Remember Me'.
        3. Click the Login button.
        4. Close and reopen browser, navigate to site.
        5. Verify user is auto-logged in.
        """
        # Credentials as per test data
        email = 'user1'
        password = 'Pass@123'
        self.login_page.login_with_remember_me_and_verify_auto_login(email, password)

    def test_TC_LOGIN_005(self):
        """
        Test Case TC_LOGIN_005: Forgot Password navigation
        Steps:
        1. Navigate to the login page.
        2. Click on 'Forgot Password' link.
        3. Verify user is redirected to password recovery page.
        """
        # Ensure navigation to login page
        self.login_page.navigate_to_login_page()
        # Click 'Forgot Password' and verify navigation
        result = self.login_page.navigate_to_forgot_password()
        assert result, "Navigation to password recovery page failed."

    def test_TC_LOGIN_006(self):
        """
        Test Case TC_LOGIN_006: SQL Injection validation
        Steps:
        1. Navigate to the login page.
        2. Enter SQL injection string in username and/or password fields.
        3. Click the Login button.
        4. Verify login fails and no unauthorized access occurs.
        """
        self.login_page.navigate_to_login_page()
        username_injection = "' OR 1=1; --"
        password_injection = "' OR 1=1; --"
        result = self.login_page.attempt_sql_injection(username_injection, password_injection)
        assert result, "SQL injection did not trigger error message or unauthorized access occurred."

    def test_TC_LOGIN_009_accessibility(self):
        """
        Test Case TC_LOGIN_009: Accessibility checks for login page.
        Steps:
        1. Navigate to the login page.
        2. Check for screen reader compatibility, keyboard navigation, and color contrast.
        3. Assert that login page is accessible as per standards.
        """
        self.login_page.navigate_to_login_page()
        result = self.login_page.check_accessibility()
        assert result, "Login page accessibility checks failed."

    def test_TC_LOGIN_010_password_masking(self):
        """
        Test Case TC_LOGIN_010: Password masking validation.
        Steps:
        1. Navigate to the login page.
        2. Enter password 'Pass@123' in the password field.
        3. Assert that password input is masked (type='password').
        """
        self.login_page.navigate_to_login_page()
        is_masked = self.login_page.enter_password('Pass@123')
        assert is_masked, "Password input is not masked (type!='password')."
