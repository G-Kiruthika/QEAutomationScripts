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

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Attempt login with empty email and valid password.
        Steps:
        1. Navigate to the login page.
        2. Leave the email field empty.
        3. Enter a valid password: ValidPass123!
        4. Click the login button.
        5. Verify error message is displayed indicating email is required.
        """
        self.login_page.navigate()
        self.login_page.enter_email('')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "Expected error message but got none."
        assert 'email' in error_message.lower(), f"Expected error about email, got: {error_message}"

    def test_TC_LOGIN_01(self):
        """
        Test Case TC-LOGIN-01: Successful login with valid credentials.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid registered email address: user@example.com
        3. Enter the correct password: ValidPassword123!
        4. Click the 'Login' button.
        5. Verify successful login and dashboard/homepage is displayed.
        """
        self.login_page.navigate()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('ValidPassword123!')
        self.login_page.click_login()
        assert self.login_page.is_login_successful(), "Login was not successful, dashboard not displayed."

    def test_TC_LOGIN_004(self):
        """
        Test Case TC_LOGIN_004: Attempt login with valid email and empty password, check for password required error.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid email address: user@example.com
        3. Leave the password field empty.
        4. Click the login button.
        5. Verify error message is displayed indicating password is required.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('')
        assert self.login_page.is_password_field_empty(), "Password field is not empty as expected."
        self.login_page.click_login_button()
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "Expected error message but got none."
        assert 'password is required' in error_message.lower(), f"Expected error about password, got: {error_message}"

    def test_TC_LOGIN_02(self):
        """
        Test Case TC-LOGIN-02: Attempt login with invalid email and valid password, check for error message.
        Steps:
        1. Navigate to the login page.
        2. Enter an invalid/unregistered email address: invaliduser@example.com
        3. Enter a valid password: ValidPassword123!
        4. Click the login button.
        5. Verify error message is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('invaliduser@example.com')
        self.login_page.enter_password('ValidPassword123!')
        self.login_page.click_login_button()
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "Expected error message but got none."
        assert 'error' in error_message.lower(), f"Expected error about login failure, got: {error_message}"

    def test_TC_LOGIN_006(self):
        """
        Test Case TC_LOGIN_006: Valid login with 'Remember Me' checked and session persistence.
        Steps:
        1. Navigate to the login page and verify it is displayed.
        2. Enter email 'user@example.com' and password 'ValidPass123!'.
        3. Check the 'Remember Me' checkbox.
        4. Click the login button and verify user is logged in.
        5. Close and reopen the browser and verify user is auto-logged in (session persists).
        """
        self.login_page.navigate_to_login_page()
        assert self.login_page.is_login_page_displayed(), "Login page is not displayed."
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.check_remember_me()
        self.login_page.click_login_button()
        assert self.login_page.is_user_logged_in(), "User is not logged in."
        # Simulate browser restart
        def driver_factory():
            from selenium import webdriver
            return webdriver.Chrome()
        new_driver = self.login_page.close_and_reopen_browser(driver_factory)
        new_login_page = LoginPage(new_driver)
        assert new_login_page.is_user_auto_logged_in(), "User is not auto-logged in after browser restart."

    def test_TC_LOGIN_04(self):
        """
        Test Case TC-LOGIN-04: Invalid login and error handling.
        Steps:
        1. Navigate to the login page and verify it is displayed.
        2. Enter email 'invaliduser@example.com' and password 'WrongPassword'.
        3. Click the login button.
        4. Verify that login fails and an error message is displayed.
        """
        self.login_page.navigate_to_login_page()
        assert self.login_page.is_login_page_displayed(), "Login page is not displayed."
        self.login_page.enter_email('invaliduser@example.com')
        self.login_page.enter_password('WrongPassword')
        self.login_page.click_login_button()
        assert self.login_page.is_error_message_displayed(), "Error message not displayed after invalid login."
        error_text = self.login_page.get_error_message_text()
        assert error_text, "Error message text is empty after invalid login."

    def test_TC_LOGIN_007(self):
        """
        Test Case TC_LOGIN_007: Password reset flow.
        Steps:
        1. Navigate to the login page.
        2. Click the 'Forgot Password' link.
        3. Enter a registered email address: user@example.com
        4. Submit the password reset request.
        5. Verify confirmation message is displayed.
        """
        self.login_page.navigate_to_login_page()
        assert self.login_page.is_login_page_displayed(), "Login page is not displayed."
        self.login_page.click_forgot_password_link()
        assert self.login_page.is_password_reset_page_displayed(), "Password reset page is not displayed."
        self.login_page.enter_reset_email('user@example.com')
        self.login_page.submit_password_reset_request()
        assert self.login_page.is_confirmation_message_displayed(), "Confirmation message is not displayed after password reset."

    def test_TC_LOGIN_05(self):
        """
        Test Case TC-LOGIN-05: Login with empty email and valid password.
        Steps:
        1. Navigate to the login page.
        2. Leave the email field empty.
        3. Enter a valid password: ValidPassword123!
        4. Click the login button.
        5. Verify error message is displayed indicating email is required.
        """
        self.login_page.navigate_to_login_page()
        assert self.login_page.is_login_page_displayed(), "Login page is not displayed."
        self.login_page.leave_email_empty()
        self.login_page.enter_password('ValidPassword123!')
        self.login_page.click_login_button()
        assert self.login_page.is_empty_field_prompt_displayed(), "Empty field prompt is not displayed for missing email."
