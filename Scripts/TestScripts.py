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
        username = 'invalid_user'
        password = 'invalid_pass'
        expected_error = 'Invalid username or password. Please try again.'
        result = self.login_page.login_with_invalid_credentials_and_verify_error(username, password, expected_error)
        assert result, f"Expected error message '{expected_error}', but got something else."

    def test_TC_LOGIN_002(self):
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_absent()

    def test_TC_LOGIN_001_valid(self):
        self.login_page.navigate_to_login_page()
        self.login_page.enter_email('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.click_login()
        assert self.login_page.verify_dashboard_header(), "Dashboard header not visible after login."

    def test_TC_LOGIN_002_invalid(self):
        self.login_page.navigate_to_login_page()
        self.login_page.enter_email('invalidUser')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login()
        assert self.login_page.verify_error_message('Invalid username or password. Please try again.'), "Error message not displayed for invalid credentials."

    def test_TC_LOGIN_003_empty_fields_error(self):
        self.login_page.login_with_empty_fields_and_verify_error()

    def test_TC_LOGIN_004_remember_me_auto_login(self):
        email = 'user1'
        password = 'Pass@123'
        self.login_page.login_with_remember_me_and_verify_auto_login(email, password)

    def test_TC_LOGIN_005(self):
        self.login_page.navigate_to_login_page()
        result = self.login_page.navigate_to_forgot_password()
        assert result, "Navigation to password recovery page failed."

    def test_TC_LOGIN_006(self):
        self.login_page.navigate_to_login_page()
        username_injection = "' OR 1=1; --"
        password_injection = "' OR 1=1; --"
        result = self.login_page.attempt_sql_injection(username_injection, password_injection)
        assert result, "SQL injection did not trigger error message or unauthorized access occurred."

    def test_TC_LOGIN_009(self):
        """
        Test Case TC_LOGIN_009: Accessibility validation
        Steps:
        1. Navigate to the login page.
        2. Check for screen reader compatibility, keyboard navigation, and color contrast.
        """
        self.login_page.navigate_to_login_page()
        screen_reader_compatible = self.login_page.is_screen_reader_compatible()
        keyboard_nav_accessible = self.login_page.is_keyboard_navigation_accessible()
        color_contrast_sufficient = self.login_page.is_color_contrast_sufficient()
        assert screen_reader_compatible, "Screen reader compatibility failed."
        assert keyboard_nav_accessible, "Keyboard navigation accessibility failed."
        assert color_contrast_sufficient, "Color contrast is not sufficient."

    def test_TC_LOGIN_010(self):
        """
        Test Case TC_LOGIN_010: Password masking validation
        Steps:
        1. Navigate to the login page.
        2. Enter password in the password field.
        3. Validate password input is masked.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.enter_password('Pass@123')
        masked = self.login_page.is_password_masked()
        assert masked, "Password field is not masked."
