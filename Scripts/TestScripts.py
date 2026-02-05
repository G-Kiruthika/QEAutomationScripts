# Import necessary modules
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    async def test_empty_fields_validation(self):
        self.login_page.navigate_to_login()
        self.login_page.enter_email('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        assert self.login_page.is_empty_field_prompt_displayed() == True

    async def test_remember_me_functionality(self):
        self.login_page.navigate_to_login()
        self.login_page.enter_email('test@example.com')
        self.login_page.enter_password('password123')
        self.login_page.toggle_remember_me(True)
        self.login_page.click_login()
        assert self.login_page.is_dashboard_header_displayed() == True

    async def test_TC_LOGIN_001_invalid_login(self):
        """
        Test Case TC_LOGIN_001:
        - Navigate to the login screen.
        - Enter an invalid username and/or password.
        - Error message 'Invalid username or password. Please try again.' is displayed.
        """
        self.login_page.navigate_to_login()
        self.login_page.enter_email('invalid@example.com')
        self.login_page.enter_password('invalidpassword')
        self.login_page.click_login()
        assert self.login_page.verify_invalid_login_error() == True
