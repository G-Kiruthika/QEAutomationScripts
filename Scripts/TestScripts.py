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
        Test Case TC_LOGIN_003: Leave email and password fields empty, click login, expect 'Mandatory fields are required' error.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.clear_username_field()
        self.login_page.clear_password_field()
        self.login_page.click_login()
        error_prompt_displayed = self.login_page.is_empty_field_prompt_displayed()
        assert error_prompt_displayed, "Expected error prompt for empty fields was not displayed."

    def test_TC_LOGIN_004(self):
        """
        Test Case TC_LOGIN_004: Enter valid credentials, check 'Remember Me', click login, close/reopen browser, navigate to site, expect user remains logged in or is auto-logged in.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.check_remember_me()
        self.login_page.click_login()
        assert self.login_page.is_user_logged_in(), "User was not logged in after checking 'Remember Me'."
        # Simulate browser restart and verify auto-login
        self.driver.quit()
        # Assuming a new driver instance is created here
        new_driver = self.create_new_driver_instance()
        new_login_page = LoginPage(new_driver)
        new_login_page.navigate_to_login_page()
        assert new_login_page.is_user_logged_in(), "User was not auto-logged in after browser restart with 'Remember Me'."

    def create_new_driver_instance(self):
        # Placeholder for actual driver instantiation logic
        pass
