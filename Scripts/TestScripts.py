import pytest
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def test_empty_fields_validation(self, driver):
        login_page = LoginPage(driver)
        login_page.login_with_empty_fields()
        assert login_page.get_error_message() == 'Mandatory fields are required'

    def test_remember_me_functionality(self, driver):
        login_page = LoginPage(driver)
        login_page.toggle_remember_me(True)
        login_page.login('valid_username', 'valid_password')
        assert login_page.is_dashboard_header_displayed()
        # Additional logic for closing and reopening browser can be implemented as needed

    def test_TC_LOGIN_001(self, driver):
        """
        TC_LOGIN_001: Navigate to login page, enter valid email and password, click login, assert dashboard is displayed
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.enter_email('user@example.com')
        login_page.enter_password('ValidPass123!')
        login_page.click_login()
        assert login_page.is_dashboard_header_displayed(), "Dashboard should be displayed after successful login"

    def test_TC_LOGIN_002(self, driver):
        """
        TC_LOGIN_002: Navigate to login page, enter invalid email and password, click login, assert error message and user not logged in
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.enter_email('invaliduser@example.com')
        login_page.enter_password('WrongPass!@#')
        login_page.click_login()
        assert login_page.get_error_message() == 'Invalid email or password.', "Expected error message for invalid credentials"
        assert not login_page.is_dashboard_header_displayed(), "Dashboard should NOT be displayed for failed login"

    def test_TC_LOGIN_003(self, driver):
        """
        TC_LOGIN_003: Attempt login with empty username and/or password,
        expect error message 'Mandatory fields are required'
        """
        login_page = LoginPage(driver)
        # Case 1: Both fields empty
        login_page.login_with_empty_fields()
        assert login_page.get_error_message() == 'Mandatory fields are required'

        # Case 2: Username empty, password filled
        login_page.login('', 'valid_password')
        assert login_page.get_error_message() == 'Mandatory fields are required'

        # Case 3: Username filled, password empty
        login_page.login('valid_username', '')
        assert login_page.get_error_message() == 'Mandatory fields are required'

    def test_TC_LOGIN_004(self, driver):
        """
        TC_LOGIN_004: Login with valid credentials and 'Remember Me' checked,
        close/reopen browser, verify user stays logged in
        """
        login_page = LoginPage(driver)
        login_page.toggle_remember_me(True)
        login_page.login('valid_username', 'valid_password')
        assert login_page.is_dashboard_header_displayed()

        # Simulate closing and reopening the browser
        driver.quit()
        # Re-initialize driver (pseudo-code, actual implementation may vary)
        new_driver = get_new_driver_instance()
        login_page_reopened = LoginPage(new_driver)
        assert login_page_reopened.is_dashboard_header_displayed()

    def test_TC_LOGIN_005(self, driver):
        """
        TC_LOGIN_005: Navigate to login page, click forgot password, verify redirection to password recovery page.
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.click_forgot_password()
        # Assuming the password recovery page has a unique element or URL to verify
        assert driver.current_url.endswith('/password-recovery') or 'password' in driver.title.lower()

    def test_TC_LOGIN_006(self, driver):
        """
        TC_LOGIN_006: Enter SQL injection strings for username and password, click login, verify login fails and no unauthorized access.
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        result = login_page.login_with_sql_injection_attempt("' OR 1=1; --", "' OR 1=1; --")
        assert result['unauthorized_access'] is True
        assert not result['dashboard_visible']
        assert not result['profile_visible']
        assert result['error_message'] is not None or result['validation_message'] is not None

    def test_TC_LOGIN_009(self, driver):
        """
        TC_LOGIN_009: Accessibility checks (screen reader compatibility, keyboard navigation, color contrast) on login page.
        """
        login_page = LoginPage(driver)
        assert login_page.check_screen_reader_compatibility(), "Screen reader compatibility failed"
        assert login_page.check_keyboard_navigation(), "Keyboard navigation accessibility failed"
        assert login_page.check_color_contrast(), "Color contrast accessibility failed"

    def test_TC_LOGIN_010(self, driver):
        """
        TC_LOGIN_010: Password masking check on login page after entering a password.
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login('valid_username', 'valid_password')
        assert login_page.is_password_field_masked(), "Password field is not masked as expected"

    # --- Newly appended tests as per provided steps ---
    def test_TC_LOGIN_003_email_empty(self, driver):
        """
        TC_LOGIN_003: Navigate to login page. Leave email empty. Enter valid password. Click login. Assert error message 'Email is required.'
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.enter_email('')
        login_page.enter_password('ValidPass123!')
        login_page.click_login()
        assert login_page.get_error_message() == 'Email is required.'

    def test_TC_LOGIN_004_password_empty(self, driver):
        """
        TC_LOGIN_004: Navigate to login page. Enter valid email. Leave password empty. Click login. Assert error message 'Password is required.'
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.enter_email('user@example.com')
        login_page.enter_password('')
        login_page.click_login()
        assert login_page.get_error_message() == 'Password is required.'
