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
        # Existing test logic for TC_LOGIN_001
        pass

    def test_TC_LOGIN_002(self, driver):
        # Existing test logic for TC_LOGIN_002
        pass

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
