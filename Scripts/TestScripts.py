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
        username = 'user1'
        password = 'Pass@123'
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        assert self.login_page.is_dashboard_displayed(), 'Dashboard not displayed after valid login.'

    def test_TC_LOGIN_002(self):
        username = 'invalidUser'
        password = 'WrongPass'
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message is not None and 'invalid' in error_message.lower(), 'Error message not displayed for invalid credentials.'

    def test_TC_LOGIN_001_valid(self):
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username('user@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        dashboard_header = self.login_page.driver.find_element(*self.login_page.dashboard_header)
        assert dashboard_header.is_displayed(), 'Dashboard header not visible after login.'

    def test_TC_LOGIN_002_invalid(self):
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username('invaliduser@example.com')
        self.login_page.enter_password('WrongPass!@#')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message == 'Invalid email or password.', 'Error message not displayed for invalid credentials.'

    def test_TC_LOGIN_003_empty_fields_error(self):
        self.login_page.login_with_empty_fields_and_verify_error()

    def test_TC_LOGIN_004_remember_me_auto_login(self):
        email = 'user1'
        password = 'Pass@123'
        self.login_page.login_with_remember_me_and_verify_auto_login(email, password)

    def test_TC_LOGIN_005(self):
        self.login_page.navigate_to_login_page()
        result = self.login_page.click_forgot_password()
        assert result, "Navigation to password recovery page failed."

    def test_TC_LOGIN_006(self):
        self.login_page.navigate_to_login_page()
        username_injection = "' OR 1=1; --"
        password_injection = "' OR 1=1; --"
        result = self.login_page.attempt_sql_injection(username_injection, password_injection)
        assert result, "SQL injection did not trigger error message or unauthorized access occurred."

    def test_TC_LOGIN_009(self):
        self.login_page.navigate_to_login_page()
        screen_reader_compatible = self.login_page.is_screen_reader_compatible()
        keyboard_nav_accessible = self.login_page.is_keyboard_navigation_accessible()
        color_contrast_sufficient = self.login_page.is_color_contrast_sufficient()
        assert screen_reader_compatible, "Screen reader compatibility failed."
        assert keyboard_nav_accessible, "Keyboard navigation accessibility failed."
        assert color_contrast_sufficient, "Color contrast is not sufficient."

    def test_TC_LOGIN_010(self):
        self.login_page.navigate_to_login_page()
        self.login_page.enter_password('Pass@123')
        masked = self.login_page.is_password_masked()
        assert masked, "Password field is not masked."

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Leave email field empty, enter valid password, click login, expect 'Email is required.' error.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.clear_email_field()
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        error_displayed = self.login_page.wait_for_error_message(expected_text='Email is required.')
        assert error_displayed, "Expected error message 'Email is required.' was not displayed."

    def test_TC_LOGIN_004(self):
        """
        Test Case TC_LOGIN_004: Enter valid email, leave password field empty, click login, expect 'Password is required.' error.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username('user@example.com')
        self.login_page.clear_password_field()
        self.login_page.click_login()
        error_displayed = self.login_page.wait_for_error_message(expected_text='Password is required.')
        assert error_displayed, "Expected error message 'Password is required.' was not displayed."

    def test_TC_LOGIN_007(self):
        """
        Test Case TC_LOGIN_007: Forgot Password flow
        1. Navigate to the login page.
        2. Click the 'Forgot Password?' link.
        3. Verify the presence of email input and reset instructions.
        """
        self.login_page.navigate_to_login_page()
        forgot_page_result = self.login_page.click_forgot_password()
        assert forgot_page_result, "Failed to navigate to Forgot Password page."
        presence_verified = self.login_page.verify_forgot_password_page()
        assert presence_verified, "Forgot Password page does not display email input and instructions."

    def test_TC_LOGIN_008(self):
        """
        Test Case TC_LOGIN_008: Login with maximum allowed email length
        1. Navigate to the login page.
        2. Enter maximum allowed length email.
        3. Enter a valid password.
        4. Click the 'Login' button.
        """
        self.login_page.navigate_to_login_page()
        max_email_entered = self.login_page.enter_max_length_email()
        assert max_email_entered, "Email field did not accept maximum allowed length."
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        login_success = False
        try:
            login_success = self.login_page.driver.find_element(*self.login_page.dashboard_header).is_displayed()
        except Exception:
            login_success = False
        assert login_success, "Login failed or dashboard not displayed with maximum email length."
