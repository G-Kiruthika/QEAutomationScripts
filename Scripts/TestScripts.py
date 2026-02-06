# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.ForgotPasswordPage import ForgotPasswordPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.forgot_password_page = ForgotPasswordPage(driver)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

    def test_TC_LOGIN_001(self):
        """Test invalid login and error message for TC-LOGIN_001"""
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
        Test Case TC-LOGIN-005: Valid email, password field empty, verify validation error and no authentication attempt
        Steps:
        1. Navigate to the login page (URL: https://ecommerce.example.com/login)
        2. Enter valid registered email address (testuser@example.com)
        3. Leave password field empty
        4. Click the Login button
        5. Assert validation error is displayed: 'Password field is required' or 'Please enter your password'
        6. Verify user remains on login page, no authentication attempt made
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_email('testuser@example.com')
        self.login_page.clear_password()
        self.login_page.click_login()
        assert self.login_page.is_password_field_empty(), "Password field is not empty after clearing."
        assert self.login_page.is_validation_error_for_password_required(), "Validation error for empty password was not displayed."
        assert self.login_page.is_login_not_processed(), "User did not remain on the login page; authentication may have been attempted."

    def test_TC_LOGIN_007(self):
        """
        Test Case TC-LOGIN-007: Verify session persistence with 'Remember Me' checked
        Steps:
        1. Navigate to login page
        2. Enter valid credentials (testuser@example.com / ValidPass123!)
        3. Check 'Remember Me'
        4. Log in
        5. Save cookies
        6. Close and reopen browser
        7. Load cookies
        8. Navigate to app URL
        9. Verify user is logged in (dashboard visible)
        """
        # Step 1: Navigate to login page
        self.login_page.navigate_to_login()
        # Step 2: Enter valid credentials
        self.login_page.enter_email('testuser@example.com')
        self.login_page.enter_password('ValidPass123!')
        # Step 3: Check 'Remember Me'
        self.login_page.check_remember_me()
        # Step 4: Log in
        self.login_page.click_login()
        # Step 5: Save cookies
        self.login_page.save_cookies('cookies.pkl')
        # Step 6: Close and reopen browser
        self.driver.quit()
        from selenium import webdriver
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        # Step 7: Load cookies
        self.login_page.load_cookies('cookies.pkl')
        # Step 8: Navigate to app URL
        self.driver.get('https://ecommerce.example.com/dashboard')
        # Step 9: Verify user is logged in (dashboard visible)
        assert self.login_page.is_logged_in(), "Session did not persist after browser restart with 'Remember Me' checked."

    def test_TC_LOGIN_009(self):
        """
        Test Case TC-LOGIN-009: Forgot Password link and recovery page verification
        Steps:
        1. Navigate to login page (URL: https://ecommerce.example.com/login)
        2. Verify 'Forgot Password' link is visible and clickable
        3. Click 'Forgot Password' link
        4. Verify navigation to password recovery page (URL: https://ecommerce.example.com/forgot-password)
        5. Verify password recovery page displays email input field and submit button
        """
        # Step 1: Navigate to login page
        self.login_page.navigate_to_login_page()
        # Step 2: Verify 'Forgot Password' link is visible and clickable
        assert self.login_page.is_forgot_password_link_present_and_clickable(), "Forgot Password link is not visible or clickable."
        # Step 3: Click 'Forgot Password' link
        self.login_page.click_forgot_password_link()
        # Step 4 & 5: Verify password recovery page elements
        assert self.login_page.verify_password_recovery_page_elements(), "Password recovery page elements are not displayed as expected."

    def test_TC_LOGIN_012(self):
        """
        Test Case TC-LOGIN-012: Login with email and password containing special characters, verify authentication result
        Steps:
        1. Navigate to the login page (URL: https://ecommerce.example.com/login)
        2. Enter email with special characters: test.user+tag@example.com
        3. Enter password with special characters: P@ssw0rd!#$%^&*()
        4. Click the Login button
        5. Verify authentication result: login succeeds if credentials are valid (dashboard and profile icon visible), fails appropriately if invalid, no system errors
        """
        self.login_page.navigate_to_login('https://ecommerce.example.com/login')
        self.login_page.enter_email('test.user+tag@example.com')
        self.login_page.enter_password('P@ssw0rd!#$%^&*()')
        self.login_page.click_login()
        # Check for success
        if self.login_page.verify_login_success():
            assert self.login_page.verify_login_success(), "Login should succeed with valid credentials containing special characters."
        else:
            error_message = self.login_page.verify_login_failure()
            assert error_message is not None, "Login failed but no error message was shown."
            assert 'error' in error_message.lower(), "Expected an error message indicating login failure."

    def test_TC_LOGIN_014(self):
        """
        Test Case TC-LOGIN-014: Login with leading/trailing spaces in email and password
        Steps:
        1. Navigate to the login page (URL: https://ecommerce.example.com/login)
        2. Enter valid email with leading/trailing spaces: '  testuser@example.com  '
        3. Enter valid password with leading/trailing spaces: '  ValidPass123!  '
        4. Click the Login button
        5. Verify authentication behavior: login succeeds if system trims spaces, or fails with a clear message if not allowed
        """
        email = '  testuser@example.com  '
        password = '  ValidPass123!  '
        # Use the LoginPage's login_with_spaces method
        result = self.login_page.login_with_spaces(email, password)
        # Assert the expected behavior
        if result['login_success']:
            assert result['login_success'], "Login should succeed if spaces are trimmed automatically."
        else:
            assert result['error_message'] or result['validation_error'] or result['empty_prompt'], "A clear validation or error message should be shown if login fails due to spaces."
