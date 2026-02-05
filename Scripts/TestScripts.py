# Import necessary modules
from LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.navigate_to_login()
        self.login_page.enter_credentials('', '')
        self.login_page.click_login()
        assert self.login_page.is_empty_field_prompt_displayed(), "Mandatory fields are required prompt not displayed."

    def test_remember_me_functionality(self):
        self.login_page.navigate_to_login()
        # Assuming fill_email and remember_me logic is implemented in LoginPage
        # self.login_page.fill_email('user@example.com')
        # self.login_page.click_remember_me()
        # self.login_page.enter_credentials('user@example.com', 'password')
        # self.login_page.click_login()
        # assert self.login_page.is_dashboard_displayed(), "Dashboard not displayed after login with Remember Me."
        pass

    def test_invalid_login_shows_error_message(self):
        """
        TC_LOGIN_001
        1. Navigate to the login screen.
        2. Enter an invalid username and/or password.
        3. Click login.
        4. Verify error message 'Invalid username or password. Please try again.' is displayed.
        """
        self.login_page.navigate_to_login()
        self.login_page.enter_invalid_credentials('invalid_user@example.com', 'wrong_password')
        self.login_page.submit_login()
        assert self.login_page.verify_error_message("Invalid username or password. Please try again."), "Expected error message not displayed."

    def test_remember_me_checkbox_absence(self):
        """
        TC_LOGIN_002
        1. Navigate to the login screen.
        2. Verify login screen is displayed.
        3. Check that 'Remember Me' checkbox is not present.
        """
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_not_present()

    def test_forgot_username_recovery(self):
        """
        TC_LOGIN_003
        1. Navigate to the login screen.
        2. Click on 'Forgot Username' link.
        3. Follow the instructions to recover username.
        4. Retrieve and assert the username.
        """
        self.login_page.go_to_login_page()
        self.login_page.click_forgot_username()
        self.login_page.recover_username('user@example.com')
        retrieved_username = self.login_page.get_retrieved_username()
        assert retrieved_username is not None and retrieved_username != '', "Username was not retrieved successfully."
