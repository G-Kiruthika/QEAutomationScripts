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
        """
        Test Case TC_LOGIN_001: Valid login and dashboard verification.
        Steps:
        1. Navigate to the login page.
        2. Enter valid username and password (user1/Pass@123).
        3. Click the Login button.
        4. Verify dashboard is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.click_login_button()
        assert self.login_page.is_dashboard_displayed(), "Dashboard should be displayed after valid login."

    def test_TC_LOGIN_002(self):
        """
        Test Case TC_LOGIN_002: Invalid login and error message verification.
        Steps:
        1. Navigate to the login page.
        2. Enter invalid username and password (invalidUser/WrongPass).
        3. Click the Login button.
        4. Verify error message is displayed.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('invalidUser')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login_button()
        assert self.login_page.is_error_message_displayed(), "Error message should be displayed for invalid login."

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Attempt login with empty fields and verify error message.
        Steps:
        1. Navigate to the login page.
        2. Leave username and password fields empty.
        3. Click the Login button.
        4. Assert error message for empty fields.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('')
        self.login_page.enter_password('')
        self.login_page.click_login_button()
        error_msg = self.login_page.get_error_message()
        assert error_msg == "Mandatory fields are required", f"Expected error message for empty fields, got: {error_msg}"

    def test_TC_LOGIN_004(self):
        """
        Test Case TC_LOGIN_004: Login with valid credentials, check 'Remember Me', close and reopen browser, assert session persistence.
        Steps:
        1. Navigate to the login page.
        2. Enter valid username and password (user1/Pass@123).
        3. Check 'Remember Me'.
        4. Click the Login button.
        5. Close and reopen browser.
        6. Assert session persistence.
        """
        self.login_page.go_to_login_page()
        self.login_page.enter_username('user1')
        self.login_page.enter_password('Pass@123')
        self.login_page.check_remember_me()
        self.login_page.click_login_button()
        assert self.login_page.is_dashboard_displayed(), "Dashboard should be displayed after login."
        # Simulate closing and reopening the browser
        self.driver.quit()
        from selenium import webdriver
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.login_page.go_to_login_page()
        session_persistent = self.login_page.is_session_persistent()
        assert session_persistent, "Session should persist after browser reopen when 'Remember Me' is checked."
