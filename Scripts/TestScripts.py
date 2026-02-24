# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.ProfilePage import ProfilePage
from Pages.FeedbackPage import FeedbackPage

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
        username = 'invalid_user'
        password = 'invalid_pass'
        expected_error = 'Invalid username or password. Please try again.'
        result = self.login_page.login_with_invalid_credentials_and_verify_error(username, password, expected_error)
        assert result, f"Expected error message '{expected_error}', but got something else."

    def test_TC_LOGIN_002(self):
        """
        Test Case TC_LOGIN_002: Navigate to login screen and verify 'Remember Me' checkbox is absent.
        Steps:
        1. Navigate to the login screen.
        2. Assert that 'Remember Me' checkbox is not present.
        """
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_absent()

class TestFeedbackFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.profile_page = ProfilePage(driver)
        self.feedback_page = FeedbackPage(driver)

    def test_HAP_21_TS_001_TC_001(self):
        """
        Test Case HAP-21 TS-001 TC-001: MyHP Feedback Flow
        Steps:
        1. Launch the MyHP app (main screen loads).
        2. Tap the Profile icon.
        3. Tap the Send Feedback button.
        4. Select the 4th star rating.
        5. Deselect the 4th star rating.
        """
        # Step 1: App launch is assumed (driver already initialized)
        # Step 2: Tap the Profile icon
        self.profile_page.tap_profile_icon()
        # Step 3: Tap the Send Feedback button
        self.profile_page.tap_send_feedback()
        # Step 4: Select the 4th star rating
        self.feedback_page.select_star_rating(4)
        # Step 5: Deselect the 4th star rating
        self.feedback_page.deselect_star_rating(4)
