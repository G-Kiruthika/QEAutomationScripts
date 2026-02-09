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

    def test_TC_LOGIN_007_rapid_incorrect_logins_account_lock_captcha(self):
        """
        Test Case TC_LOGIN_007: Rapid incorrect logins, account lock/CAPTCHA detection
        Steps:
        1. Attempt 10 rapid logins with incorrect credentials (user1/wrongPass)
        2. Observe system response for account lock or CAPTCHA
        """
        username = 'user1'
        password = 'wrongPass'
        attempts = 10
        interval = 0.2  # seconds between attempts
        self.login_page.attempt_multiple_logins(username, password, attempts, interval)
        account_locked = self.login_page.is_account_locked()
        captcha_present = self.login_page.is_captcha_present()
        assert account_locked or captcha_present, 'Account should be locked or CAPTCHA should be triggered after rapid incorrect logins.'
        if account_locked:
            print('Account lock detected.')
        if captcha_present:
            print('CAPTCHA detected.')

    def test_TC_LOGIN_008_rapid_valid_logins_response_time(self):
        """
        Test Case TC_LOGIN_008: Rapid valid logins, response time measurement
        Steps:
        1. Attempt 10 rapid valid logins (user1/Pass@123)
        2. Measure response time for each login
        """
        username = 'user1'
        password = 'Pass@123'
        attempts = 10
        interval = 0.2  # seconds between attempts
        response_times = self.login_page.attempt_multiple_valid_logins(username, password, attempts, interval)
        assert len(response_times) == attempts, f'Expected {attempts} response times, got {len(response_times)}.'
        for i, resp_time in enumerate(response_times):
            assert resp_time < 5.0, f'Login response time {resp_time:.2f}s for attempt {i+1} exceeds threshold.'
        print(f'All login response times: {response_times}')
