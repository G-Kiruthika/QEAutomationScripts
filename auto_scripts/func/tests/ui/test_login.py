"""Login Test Suite

This module contains automated test cases for the Login functionality.
Follows the Python UI & API Automation Framework standards.
"""

import pytest
from core.driver_factory import get_driver
from pages.login_page import LoginPage


class TestLogin:
    """Test class for Login functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method to initialize driver and page objects before each test"""
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)
        yield
        self.driver.quit()

    def test_tc_pos_001_valid_login(self):
        """Test Case: TC_POS_001 - Valid Login
        
        Validates successful login with valid credentials.
        Verifies user authentication, username display, and session token generation.
        """
        # Test data
        url = "https://ecommerce.example.com/login"
        email = "testuser@example.com"
        password = "Test@1234"
        
        # Test flow
        self.login_page.navigate_to_login_page(url)
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.login_page.click_login_button()
        
        # Assertions
        assert self.login_page.is_user_authenticated(), "User authentication failed"
        assert self.login_page.is_user_name_displayed(), "User name is not displayed"
        assert self.login_page.is_session_token_generated(), "Session token was not generated"

    def test_tc_login_006_invalid_login(self):
        """Test Case: TC_LOGIN_006 - Invalid Login
        
        Validates error handling for invalid login credentials.
        Verifies error message display and user remains on login page.
        """
        # Test data
        url = "https://ecommerce-website.com/login"
        username = "invaliduser@example.com"
        password = "ValidPass123!"
        
        # Test flow
        self.login_page.navigate_to_login_page(url)
        self.login_page.enter_email(username)
        self.login_page.enter_password(password)
        self.login_page.click_login_button()
        
        # Assertions
        assert self.login_page.is_error_message_displayed(), "Error message is not displayed"
        assert self.login_page.is_on_login_page(), "User is not on login page"
