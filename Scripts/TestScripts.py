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
        """Test invalid login and error message for TC_LOGIN_001"""
        # Step 1: Navigate to login screen
        self.login_page.go_to_login_page()
        # Step 2: Enter invalid username/password
        username = 'invalid_user'
        password = 'invalid_pass'
        self.login_page.perform_invalid_login(username, password)
        # Step 3: Verify error message
        expected_error = 'Invalid username or password. Please try again.'
        self.login_page.assert_error_message_displayed(expected_error)

    def test_TC_LOGIN_002(self):
        """
        Test Case TC_LOGIN_002: Navigate to login screen and verify 'Remember Me' checkbox is absent.
        Steps:
        1. Navigate to the login screen.
        2. Assert that 'Remember Me' checkbox is not present.
        """
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_absent()

    def test_TC_LOGIN_003(self):
        """
        Test Case TC_LOGIN_003: Forgot Username workflow
        Steps:
        1. Navigate to the login screen.
        2. Click on 'Forgot Username' link.
        3. Follow the instructions to recover username.
        4. Retrieve the username and assert it is displayed.
        """
        # Step 1: Navigate to login screen
        self.login_page.go_to_login_page()
        # Step 2: Click on 'Forgot Username' link
        self.login_page.click_forgot_username()
        # Step 3: Follow instructions to recover username
        self.login_page.follow_recovery_instructions()
        # Step 4: Retrieve the username and assert it is displayed
        retrieved_username = self.login_page.retrieve_username()
        assert retrieved_username is not None and retrieved_username != "", "Username should be retrieved and displayed"
