# Import necessary modules
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver, locators=None):
        self.driver = driver
        if locators:
            self.login_page = LoginPage(driver, locators)
        else:
            self.login_page = LoginPage(driver)

    def test_TC_LOGIN_003_empty_fields_prompt(self):
        """
        Test Case TC_LOGIN_003: Validate error prompt for empty fields
        Steps:
        1. Navigate to the login page.
        2. Leave username and/or password fields empty.
        3. Click the Login button.
        4. Verify error message is displayed prompting to fill in required fields.
        """
        self.login_page.go_to_login_page()
        error_prompt = self.login_page.verify_empty_fields_error()
        assert error_prompt == 'Mandatory fields are required', f'Expected "Mandatory fields are required", got: {error_prompt}'

    def test_TC_LOGIN_004_remember_me_auto_login(self):
        """
        Test Case TC_LOGIN_004: Validate Remember Me and auto-login
        Steps:
        1. Navigate to the login page.
        2. Enter valid credentials and check "Remember Me" option.
        3. Click the Login button.
        4. Close and reopen the browser, navigate to the site.
        5. Verify user remains logged in or is auto-logged in.
        """
        self.login_page.go_to_login_page()
        self.login_page.perform_login_with_remember_me('user1', 'Pass@123')
        assert self.login_page.is_user_auto_logged_in(), 'User should remain logged in or be auto-logged in after browser restart.'

    def test_TC_LOGIN_009_accessibility(self):
        """
        Test Case TC_LOGIN_009: Accessibility validation
        Steps:
        1. Navigate to the login page.
        2. Check for screen reader compatibility, keyboard navigation, and color contrast.
        """
        self.login_page.go_to_login_page()
        report = self.login_page.check_accessibility_features()
        assert report['email_aria'], 'Email field should have ARIA label.'
        assert report['password_aria'], 'Password field should have ARIA label.'
        assert report['login_button_aria'], 'Login button should have ARIA label.'
        assert report['email_tabindex'], 'Email field should be keyboard accessible.'
        assert report['password_tabindex'], 'Password field should be keyboard accessible.'
        assert report['login_button_tabindex'], 'Login button should be keyboard accessible.'
        # Optionally, check color values (not asserting, just logging)
        print('Email field color:', report['email_color'], '| Background:', report['email_bg'])
        print('Password field color:', report['password_color'], '| Background:', report['password_bg'])
        print('Login button color:', report['login_button_color'], '| Background:', report['login_button_bg'])

    def test_TC_LOGIN_010_password_masking(self):
        """
        Test Case TC_LOGIN_010: Password masking validation
        Steps:
        1. Navigate to the login page.
        2. Enter password in the password field and verify it is masked.
        """
        self.login_page.go_to_login_page()
        is_masked = self.login_page.validate_password_masking()
        assert is_masked, 'Password input should be masked (type="password").'
