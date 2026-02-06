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
        Test Case TC-LOGIN-007: Remember Me - Session Persistence
        Steps:
        1. Navigate to the login page
        2. Enter valid email and password
        3. Check the 'Remember Me' checkbox
        4. Log in
        5. Save cookies
        6. Close and reopen browser (simulate by new driver instance)
        7. Load cookies
        8. Navigate to the app URL
        9. Verify user is automatically logged in and redirected to dashboard
        """
        # Step 1-4: Login with Remember Me
        self.login_page.go_to_login_page()
        self.login_page.enter_email('testuser@example.com')
        self.login_page.enter_password('ValidPassword123!')
        self.login_page.check_remember_me()
        self.login_page.click_login()
        assert self.login_page.is_logged_in(), "Login failed with valid credentials and Remember Me checked."

        # Step 5: Save cookies
        cookies = self.login_page.get_cookies()

        # Step 6: Simulate browser close and reopen (new driver instance)
        self.driver.quit()
        from selenium import webdriver
        self.driver = webdriver.Chrome()  # Or whichever driver is appropriate
        self.login_page = LoginPage(self.driver)

        # Step 7: Load cookies
        self.login_page.driver.get("https://example-ecommerce.com")  # Must open domain before adding cookies
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        # Step 8: Navigate to the app URL (dashboard)
        self.login_page.driver.get("https://example-ecommerce.com/dashboard")

        # Step 9: Verify user is automatically logged in and redirected to dashboard
        assert self.login_page.is_logged_in(), "User was not automatically logged in after loading cookies."
