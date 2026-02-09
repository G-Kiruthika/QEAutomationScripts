# Import necessary modules
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
    # ... existing methods ...

    def test_TC_LOGIN_003_email_required(self):
        '''
        TC_LOGIN_003: 
        1. Navigate to login page
        2. Leave email empty
        3. Enter valid password
        4. Click login
        5. Verify error message about email required
        '''
        self.login_page.navigate_to_login_page()
        self.login_page.enter_email("")
        self.login_page.enter_password("ValidPassword123")
        self.login_page.click_login()
        error_msg = self.login_page.get_error_message()
        assert "Email is required" in error_msg, f"Expected email required error, got: {error_msg}"

    def test_TC_LOGIN_01_successful_login(self):
        '''
        TC-LOGIN-01:
        1. Navigate to login page
        2. Enter valid email
        3. Enter correct password
        4. Click login
        5. Verify successful login and dashboard/homepage is displayed
        '''
        self.login_page.navigate_to_login_page()
        self.login_page.enter_email("valid.user@example.com")
        self.login_page.enter_password("ValidPassword123")
        self.login_page.click_login()
        assert self.login_page.is_dashboard_displayed(), "Dashboard/Homepage was not displayed after login"
