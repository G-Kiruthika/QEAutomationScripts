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

    # TC_LOGIN_008: Email min/max validation
    def test_TC_LOGIN_008(self):
        """
        Test Case TC_LOGIN_008: Email minimum and maximum length validation.
        Steps:
        1. Navigate to the login page and verify it is displayed.
        2. Enter email less than minimum allowed ('a@b.c'), verify validation error.
        3. Enter email at maximum allowed (64 'a's + '@example.com'), verify acceptance.
        4. Enter email exceeding maximum (65 'a's + '@example.com'), verify validation error.
        """
        self.login_page.load()
        assert self.login_page.is_displayed(), "Login page is not displayed."

        # Step 2: Minimum email length
        min_email = 'a@b.c'
        self.login_page.enter_email(min_email)
        self.login_page.enter_password('ValidPassword123!')
        self.login_page.click_login()
        validation_error = self.login_page.get_validation_error()
        assert validation_error is not None, "Expected validation error for minimum length but got none."
        assert 'minimum' in validation_error.lower(), f"Expected minimum length error, got: {validation_error}"

        # Step 3: Maximum allowed email
        max_email = 'a' * 64 + '@example.com'
        self.login_page.clear_email()
        self.login_page.enter_email(max_email)
        self.login_page.enter_password('ValidPassword123!')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message is None or 'maximum' not in error_message.lower(), f"Unexpected error for maximum allowed email: {error_message}"

        # Step 4: Exceed maximum allowed email
        over_max_email = 'a' * 65 + '@example.com'
        self.login_page.clear_email()
        self.login_page.enter_email(over_max_email)
        self.login_page.enter_password('ValidPassword123!')
        self.login_page.click_login()
        validation_error = self.login_page.get_validation_error()
        assert validation_error is not None, "Expected validation error for maximum length but got none."
        assert 'maximum' in validation_error.lower(), f"Expected maximum length error, got: {validation_error}"

    # TC-LOGIN-06: Empty password error
    def test_TC_LOGIN_06(self):
        """
        Test Case TC-LOGIN-06: Empty password error validation.
        Steps:
        1. Navigate to the login page and verify it is displayed.
        2. Enter a valid email ('user@example.com').
        3. Leave password empty.
        4. Click login and verify error for missing password.
        """
        self.login_page.load()
        assert self.login_page.is_displayed(), "Login page is not displayed."
        self.login_page.enter_email('user@example.com')
        self.login_page.clear_password()
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "Expected error message for empty password but got none."
        assert 'password' in error_message.lower() or 'required' in error_message.lower(), f"Expected password required error, got: {error_message}"

    # TC_LOGIN_009: Password min/max/exceed validation
    def test_TC_LOGIN_009(self):
        """
        Test Case TC_LOGIN_009: Password minimum, maximum, and exceeding maximum length validation.
        Steps:
        1. Navigate to the login page and verify it is displayed.
        2. Enter password with less than minimum allowed characters (e.g., '123'). Verify validation error for minimum length.
        3. Enter password with maximum allowed characters (e.g., 'A'). Verify password is accepted.
        4. Enter password exceeding maximum allowed characters (e.g., 'A'). Verify validation error for maximum length.
        """
        self.login_page.navigate_to_login_page()
        assert self.login_page.is_login_page_displayed(), "Login page is not displayed."
        # Step 2: Min length
        self.login_page.enter_password_min_length('123')
        self.login_page.click_login_button()
        assert self.login_page.is_validation_error_displayed(), "Validation error for minimum length not displayed."
        assert 'minimum' in self.login_page.get_validation_error_text().lower(), f"Expected minimum length error, got: {self.login_page.get_validation_error_text()}"
        # Step 3: Max length
        self.login_page.enter_password_max_length('A')
        self.login_page.click_login_button()
        assert self.login_page.is_password_accepted('A'), "Password not accepted at maximum length."
        # Step 4: Exceed max length
        self.login_page.enter_password_exceed_max_length('A')
        self.login_page.click_login_button()
        assert self.login_page.is_validation_error_displayed(), "Validation error for maximum length not displayed."
        assert 'maximum' in self.login_page.get_validation_error_text().lower(), f"Expected maximum length error, got: {self.login_page.get_validation_error_text()}"

    # TC-LOGIN-07: Empty fields, login button, error message
    def test_TC_LOGIN_07(self):
        """
        Test Case TC-LOGIN-07: Leave both email and password fields empty, click login, validate error messages.
        Steps:
        1. Navigate to the login page and verify it is displayed.
        2. Leave both email and password fields empty.
        3. Click the 'Login' button.
        4. Verify login fails and appropriate error messages are displayed indicating both fields are required.
        """
        self.login_page.navigate_to_login_page()
        assert self.login_page.is_login_page_displayed(), "Login page is not displayed."
        # Step 2: Leave both fields empty
        assert self.login_page.is_email_field_empty(), "Email field is not empty."
        assert self.login_page.is_password_field_empty(), "Password field is not empty."
        # Step 3: Click login
        self.login_page.click_login_button()
        # Step 4: Validate error messages
        assert self.login_page.is_empty_field_prompt_displayed(), "Error message for empty fields not displayed."
        error_text = self.login_page.get_error_message_text()
        assert 'required' in error_text.lower(), f"Expected error about required fields, got: {error_text}"
