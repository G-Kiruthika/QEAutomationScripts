# Import necessary modules
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
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

    def test_TC_LOGIN_009_accessibility_validation(self):
        """
        Test Case TC_LOGIN_009: Accessibility validation for login page
        Steps:
        1. Navigate to the login page.
        2. Check for screen reader compatibility, keyboard navigation, and color contrast.
        """
        self.login_page.navigate()
        accessibility_results = self.login_page.validate_accessibility()
        assert accessibility_results["email_aria_label"], "Email field should have aria-label for screen readers"
        assert accessibility_results["password_aria_label"], "Password field should have aria-label for screen readers"
        assert accessibility_results["login_btn_aria_label"], "Login button should have aria-label for screen readers"
        tab_order = accessibility_results["tab_order"]
        assert tab_order == ["login-email", "login-password", "login-submit"], f"Tab order should be email -> password -> login, got: {tab_order}"
        color_contrast = accessibility_results["color_contrast"]
        for field_id, contrast in color_contrast.items():
            assert contrast["fg"] != contrast["bg"], f"Foreground and background color should be different for {field_id}"

    def test_TC_LOGIN_010_password_masking(self):
        """
        Test Case TC_LOGIN_010: Password masking check
        Steps:
        1. Navigate to the login page.
        2. Enter password in the password field.
        """
        self.login_page.navigate()
        self.login_page.enter_password("Pass@123")
        is_masked = self.login_page.is_password_masked()
        assert is_masked, "Password input should be masked (type='password')"
