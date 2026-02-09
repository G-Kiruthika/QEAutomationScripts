# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.ProfilePage import ProfilePage

class TestLoginFunctionality:
    def __init__(self, driver, locators=None):
        self.driver = driver
        if locators:
            self.login_page = LoginPage(driver, locators)
        else:
            self.login_page = LoginPage(driver)

    def test_TC_LOGIN_003_empty_fields_prompt(self):
        ...
    def test_TC_LOGIN_004_remember_me_auto_login(self):
        ...
    def test_TC_LOGIN_009_accessibility(self):
        ...
    def test_TC_LOGIN_010_password_masking(self):
        ...

    def test_TC_LOGIN_001_valid_login(self):
        """
        Test Case TC_LOGIN_001: Valid login scenario
        Steps:
        1. Navigate to the login page.
        2. Enter a valid registered email address in the email field.
        3. Enter a valid password in the password field.
        4. Click the 'Login' button.
        5. Verify user is logged in and redirected to the account/dashboard page.
        """
        self.login_page.navigate()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        assert self.login_page.is_logged_in(), 'User should be logged in and dashboard should be visible.'
        profile_page = ProfilePage(self.driver, {'ProfilePage': {'profile_page_indicator': "//div[@id='profile-indicator']", 'profile_name': "//span[@id='profile-name']", 'logout_button': "//button[@id='logout-btn']"}})
        assert profile_page.is_profile_loaded(), 'Profile page should be loaded after login.'
        assert profile_page.get_profile_name() is not None, 'Profile name should be displayed.'

    def test_TC_LOGIN_002_invalid_login(self):
        """
        Test Case TC_LOGIN_002: Invalid login scenario
        Steps:
        1. Navigate to the login page.
        2. Enter an unregistered email address in the email field.
        3. Enter an incorrect password in the password field.
        4. Click the 'Login' button.
        5. Verify error message is displayed and user is not logged in.
        """
        self.login_page.navigate()
        self.login_page.enter_email('invaliduser@example.com')
        self.login_page.enter_password('WrongPass!@#')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message == 'Invalid email or password.', f'Expected "Invalid email or password.", got: {error_message}'
        assert not self.login_page.is_logged_in(), 'User should not be logged in with invalid credentials.'
