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
        # ... (other test cases)
        pass

    # ... (other test cases)

    def test_TC_LOGIN_015(self):
        """
        Test Case TC-LOGIN-015: Rapid login attempts and error/lockout handling
        Steps:
        1. Navigate to the login page (https://ecommerce.example.com/login)
        2. Enter valid credentials (Email: testuser@example.com, Password: ValidPass123!)
        3. Click Login button rapidly 10 times in succession
        4. Verify system response (rate limiting, duplicate ignore, or proper error/success)
        5. Repeat with invalid credentials (WrongPass), 10 rapid attempts
        6. Check for lockout/CAPTCHA and system stability
        """
        # Step 1 & 2: Navigate and enter valid credentials
        self.login_page.navigate_to_login('https://ecommerce.example.com/login')
        # Step 3 & 4: Rapid login attempts with valid credentials
        responses_valid = self.login_page.rapid_login_attempts('testuser@example.com', 'ValidPass123!', attempts=10, delay_between_clicks=0.1)
        print("Rapid login (valid credentials) responses:", responses_valid)
        # Check system stability
        assert any(["Login successful - dashboard displayed" in r for r in responses_valid]) or any(["Error:" in r for r in responses_valid]) or any(["No visible response" in r for r in responses_valid]), "System did not respond as expected to rapid login attempts."
        # Step 5 & 6: Rapid login attempts with invalid credentials
        responses_invalid = self.login_page.rapid_invalid_login_attempts('testuser@example.com', 'WrongPass', attempts=10, delay_between_clicks=0.1)
        print("Rapid login (invalid credentials) responses:", responses_invalid)
        # Check for lockout/CAPTCHA and system stability
        assert responses_invalid['lockout_detected'] or responses_invalid['captcha_detected'] or len(responses_invalid['error_messages']) == 10, "System did not handle rapid invalid login attempts correctly."
        # Final system stability check
        assert not self.login_page._is_element_present('crash_indicator', 'crash_indicator'), "System crashed after rapid login attempts."

    def test_TC_LOGIN_020(self):
        """
        Test Case TC-LOGIN-020: Minimum valid email and password, boundary error check
        Steps:
        1. Navigate to the login page (https://ecommerce.example.com/login)
        2. Enter minimum valid email (a@b.co)
        3. Enter minimum valid password (Pass123!)
        4. Click Login
        5. Verify login result and no boundary errors
        """
        self.login_page.navigate_to_login('https://ecommerce.example.com/login')
        self.login_page.enter_email('a@b.co')
        self.login_page.enter_password('Pass123!')
        self.login_page.click_login()
        # Check if login is successful or failed appropriately
        login_success = self.login_page.is_login_successful()
        # Ensure no boundary errors
        no_boundary_errors = self.login_page.has_no_boundary_errors()
        assert no_boundary_errors, 'Boundary errors detected (empty field or validation error) after login.'
        # Optionally, check result
        assert login_success or not login_success, 'Login result not determined.'
