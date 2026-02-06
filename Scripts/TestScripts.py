# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.PasswordRecoveryPage import PasswordRecoveryPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.password_recovery_page = PasswordRecoveryPage(driver)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

    def test_TC_LOGIN_001(self):
        username = 'invalid_user'
        password = 'invalid_pass'
        expected_error = 'Invalid username or password. Please try again.'
        result = self.login_page.login_with_invalid_credentials_and_verify_error(username, password, expected_error)
        assert result, f"Expected error message '{expected_error}', but got something else."

    def test_TC_LOGIN_002(self):
        self.login_page.go_to_login_page()
        self.login_page.assert_remember_me_checkbox_absent()

    def test_TC_LOGIN_002_invalid_email(self):
        self.login_page.go_to_login_page()
        self.login_page.enter_email('invalid@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.click_login()
        assert self.login_page.get_error_message() == 'Invalid email or password', "Error message 'Invalid email or password' was not displayed."
        assert self.login_page.is_on_login_page(), "User did not remain on the login page after invalid login attempt."

    def test_TC_LOGIN_003(self):
        self.login_page.go_to_login_page()
        self.login_page.enter_email('testuser@example.com')
        self.login_page.enter_password('WrongPassword123')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        assert error_message == 'Invalid email or password', f"Expected error message 'Invalid email or password', but got '{error_message}'."
        assert self.login_page.is_on_login_page(), "User did not remain on the login page after invalid login attempt."

    def test_TC_LOGIN_005(self):
        self.login_page.go_to_login_page()
        self.login_page.enter_email('testuser@example.com')
        self.login_page.clear_password()
        self.login_page.click_login()
        assert self.login_page.is_password_field_empty(), "Password field is not empty after clearing."
        assert self.login_page.is_validation_error_for_password_required(), "Validation error for empty password was not displayed."
        assert self.login_page.is_login_not_processed(), "User did not remain on the login page; authentication may have been attempted."

    def test_TC_LOGIN_007(self):
        self.login_page.navigate_to_login()
        self.login_page.enter_email('testuser@example.com')
        self.login_page.enter_password('ValidPass123!')
        self.login_page.check_remember_me()
        self.login_page.click_login()
        self.login_page.save_cookies('cookies.pkl')
        self.driver.quit()
        from selenium import webdriver
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.login_page.load_cookies('cookies.pkl')
        self.driver.get('https://ecommerce.example.com/dashboard')
        assert self.login_page.is_logged_in(), "Session did not persist after browser restart with 'Remember Me' checked."

    def test_TC_LOGIN_009(self):
        """
        Test Case TC-LOGIN-009: Verify 'Forgot Password' link redirects to password recovery page and required elements are present.
        Steps:
        1. Navigate to login page.
        2. Verify 'Forgot Password' link is visible and clickable.
        3. Click 'Forgot Password' link.
        4. Verify password recovery page URL.
        5. Verify email input and submit button are present.
        """
        # Step 1: Navigate to login page
        self.login_page.navigate_to_login()
        # Step 2: Verify 'Forgot Password' link is visible and clickable
        self.login_page.verify_forgot_password_link_visible()
        self.login_page.verify_forgot_password_link_clickable()
        # Step 3: Click 'Forgot Password' link
        self.login_page.click_forgot_password_link()
        # Step 4: Verify password recovery page URL
        self.password_recovery_page.verify_recovery_page_url()
        # Step 5: Verify email input and submit button are present
        self.password_recovery_page.verify_email_input_present()
        self.password_recovery_page.verify_submit_button_present()
