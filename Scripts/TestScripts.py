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

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Empty Fields Validation
        Steps:
        1. Navigate to the login page.
        2. Leave username and/or password fields empty.
        3. Click the Login button.
        4. Verify error message prompting to fill in required fields.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_credentials(username="", password="")
        self.login_page.click_login()
        error_message = self.login_page.assert_empty_field_prompt()
        assert error_message is not None and 'Mandatory fields are required' in error_message, f"Expected prompt for mandatory fields, got: {error_message}"

    def test_TC_LOGIN_004(self):
        """
        Test Case TC_LOGIN_004: Remember Me Functionality and Login Persistence
        Steps:
        1. Navigate to the login page.
        2. Enter valid credentials and check 'Remember Me'.
        3. Click the Login button.
        4. Close and reopen the browser, navigate to the site.
        5. Verify user remains logged in.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_credentials(username="user1", password="Pass@123")
        self.login_page.check_remember_me()
        self.login_page.click_login()
        assert self.login_page.is_logged_in(), "User should be logged in after valid credentials."
        self.login_page.close_and_reopen_browser()
        self.login_page.go_to_login_page()
        assert self.login_page.is_logged_in(), "User should remain logged in after browser restart with 'Remember Me' checked."

    def test_TC_LOGIN_007(self):
        """
        Test Case TC_LOGIN_007: Multiple Invalid Login Attempts and Lockout/CAPTCHA Detection
        Steps:
        1. Attempt multiple logins with incorrect credentials in rapid succession (10 times).
        2. Observe system response after threshold is reached.
        Expected: Account is locked or CAPTCHA is triggered, error message is displayed.
        """
        username = "user1"
        password = "wrongPass"
        attempts = 10
        responses = self.login_page.attempt_multiple_logins(username, password, attempts)
        locked = any(r['locked'] for r in responses)
        captcha = any(r['captcha'] for r in responses)
        errors = [r['error'] for r in responses if r['error']]
        assert locked or captcha, "Account should be locked or CAPTCHA triggered after multiple invalid logins."
        assert errors, "Error message should be displayed after invalid login attempts."

    def test_TC_LOGIN_008(self):
        """
        Test Case TC_LOGIN_008: Multiple Valid Login Attempts and Performance Measurement
        Steps:
        1. Simulate multiple valid login attempts in rapid succession.
        2. Measure response time and server load.
        Expected: Login remains responsive, no server crashes or slowdowns.
        """
        username = "user1"
        password = "Pass@123"
        attempts = 10
        results = self.login_page.attempt_multiple_valid_logins(username, password, attempts)
        response_times = [r['response_time'] for r in results if r['response_time'] is not None]
        errors = [r['error'] for r in results if r['error']]
        assert response_times, "Should have response time measurements for valid logins."
        avg_response = sum(response_times) / len(response_times) if response_times else None
        assert all(rt < 5 for rt in response_times), f"All login response times should be under 5 seconds, got: {response_times}"
        assert not errors, f"No errors should occur during valid login attempts, got: {errors}"

    # --- New methods appended below ---

    def test_TC_LOGIN_005_empty_fields(self):
        """
        Test Case TC_LOGIN_005: Both email and password fields empty
        Steps:
        1. Navigate to the login page.
        2. Leave both email and password fields empty.
        3. Click the 'Login' button.
        4. Assert error messages 'Email is required.' and 'Password is required.' are displayed. User is not logged in.
        """
        self.login_page.navigate("https://example.com/login")
        self.login_page.leave_fields_empty()
        self.login_page.click_login()
        errors = self.login_page.get_error_messages()
        assert "Email is required." in errors, f"Expected 'Email is required.' error, got: {errors}"
        assert "Password is required." in errors, f"Expected 'Password is required.' error, got: {errors}"
        assert not self.login_page.is_logged_in(), "User should not be logged in when both fields are empty."

    def test_TC_LOGIN_006_remember_me_session(self):
        """
        Test Case TC_LOGIN_006: Valid login with 'Remember Me' and session persistence
        Steps:
        1. Navigate to the login page.
        2. Enter valid email and password.
        3. Check the 'Remember Me' checkbox.
        4. Click the 'Login' button.
        5. Close and reopen the browser, revisit the site.
        6. Assert user remains logged in; session persists.
        """
        self.login_page.navigate("https://example.com/login")
        self.login_page.enter_email("user@example.com")
        self.login_page.enter_password("ValidPass123!")
        self.login_page.check_remember_me()
        assert self.login_page.is_remember_me_checked(), "'Remember Me' checkbox should be selected."
        self.login_page.click_login()
        assert self.login_page.is_logged_in(), "User should be logged in after valid credentials."
        # Simulate session persistence
        self.login_page.validate_session_persistence("https://example.com/login")
        # After browser re-initialization, check if user remains logged in
        assert self.login_page.is_logged_in(), "User should remain logged in after browser restart with 'Remember Me' checked."
