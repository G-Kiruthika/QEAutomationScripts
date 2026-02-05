# Import necessary modules
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.go_to()
        self.login_page.enter_username("")
        self.login_page.enter_password("")
        self.login_page.submit_login()
        assert self.login_page.is_empty_field_prompt_displayed(), "Mandatory fields prompt not displayed"

    def test_remember_me_functionality(self):
        self.login_page.go_to()
        self.login_page.enter_username("testuser@example.com")
        self.login_page.enter_password("testpassword")
        self.login_page.set_remember_me(True)
        self.login_page.submit_login()
        assert self.login_page.is_dashboard_loaded(), "Dashboard not loaded after login"

    def test_invalid_login_tc_login_001(self):
        """
        Test Case TC_LOGIN_001:
        - Navigate to login screen
        - Enter invalid username/password
        - Submit login
        - Assert error message 'Invalid username or password. Please try again.' is displayed
        """
        self.login_page.go_to()
        self.login_page.login_and_expect_error(
            username="invaliduser@example.com",
            password="invalidpassword",
            expected_error="Invalid username or password. Please try again."
        )

    def test_remember_me_checkbox_absent_tc_login_002(self):
        """
        Test Case TC_LOGIN_002:
        - Navigate to login screen
        - Assert that the 'Remember Me' checkbox is NOT present
        """
        self.login_page.navigate_to_login()
        assert self.login_page.is_remember_me_checkbox_absent(), "'Remember Me' checkbox should NOT be present on the login page"
