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

    def test_TC_LOGIN_016(self):
        """
        Test Case TC-LOGIN-016: Email case insensitivity and password case sensitivity
        Steps:
        1. Navigate to the login page (https://ecommerce.example.com/login)
        2. Enter email with different case than registered (Registered: testuser@example.com, Entered: TestUser@Example.com)
        3. Enter correct password (ValidPass123!)
        4. Click Login button
        5. Login should succeed (email should be case-insensitive)
        6. Test password case sensitivity: correct email, wrong case password (validpass123!)
        7. Login should fail (password should be case-sensitive)
        """
        # Step 1-5: Email case insensitivity
        registered_email = 'testuser@example.com'
        entered_email = 'TestUser@Example.com'
        correct_password = 'ValidPass123!'
        result_email_case = self.login_page.test_email_case_insensitivity(registered_email, entered_email, correct_password)
        assert result_email_case, "Login should succeed with email case-insensitive."

        # Step 6-7: Password case sensitivity
        wrong_case_password = 'validpass123!'
        result_password_case = self.login_page.test_password_case_sensitivity(registered_email, correct_password, wrong_case_password)
        assert result_password_case, "Login should fail with password case-sensitive."
