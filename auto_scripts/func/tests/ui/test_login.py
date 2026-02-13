import pytest
from core.driver_factory import get_driver
from pages.login_page import LoginPage


class TestLogin:
    """Test suite for Login functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method to initialize driver and page objects"""
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)
        yield
        self.driver.quit()

    def test_login_blank_username_tc_008(self):
        """Test Case TC_LOGIN_008: Verify login with blank username"""
        # Navigate to login page
        self.driver.get("https://ecommerce-website.com/login")
        assert self.login_page.is_login_page_displayed(), "Login page should be displayed"

        # Enter blank username
        self.login_page.enter_username("")
        assert self.login_page.is_username_blank(), "Username field should be blank"

        # Enter valid password
        self.login_page.enter_password("ValidPass123!")
        assert self.login_page.is_password_entered(), "Password should be entered"

        # Click login button
        self.login_page.click_login()

        # Verify error message
        error_message = self.login_page.get_error_message()
        assert error_message == "Username is required", f"Expected 'Username is required', but got '{error_message}'"
        assert self.login_page.is_error_message_displayed(), "Error message should be displayed"

        # Verify login is blocked
        assert self.login_page.is_login_page_displayed(), "User should remain on login page"

    def test_login_account_lockout_tc_010(self):
        """Test Case TC_LOGIN_010: Verify account lockout after multiple failed login attempts"""
        # Navigate to login page
        self.driver.get("https://ecommerce-website.com/login")
        assert self.login_page.is_login_page_displayed(), "Login page should be displayed"

        # Enter valid username
        self.login_page.enter_username("validuser@example.com")
        assert self.login_page.is_field_filled("username"), "Username field should be filled"

        # Attempt login with wrong passwords 5 times
        wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
        for wrong_password in wrong_passwords:
            self.login_page.enter_password(wrong_password)
            assert self.login_page.is_password_entered(), "Password should be entered"
            self.login_page.click_login()
            error_message = self.login_page.get_error_message()
            assert error_message == "Invalid credentials", f"Expected 'Invalid credentials', but got '{error_message}'"
            assert self.login_page.is_error_message_displayed(), "Error message should be displayed after failed attempt"

        # Attempt login with correct password after 5 failed attempts
        self.login_page.enter_password("ValidPass123!")
        assert self.login_page.is_password_entered(), "Password should be entered"
        self.login_page.click_login()

        # Verify account lockout message
        lockout_message = self.login_page.get_error_message()
        expected_lockout_message = "Account locked due to multiple failed attempts. Please try again after 30 minutes or reset password"
        assert lockout_message == expected_lockout_message, f"Expected lockout message, but got '{lockout_message}'"

        # Verify account lockout notification
        assert self.login_page.is_account_lockout_notification_displayed(), "Account lockout notification should be displayed"
