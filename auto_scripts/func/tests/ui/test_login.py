# auto_scripts/func/tests/ui/test_login.py

"""Login Test Suite

This module contains test cases for user authentication functionality.
Follows the Python UI & API Automation Framework standards.
"""

from core.driver_factory import get_driver
import logging

logger = logging.getLogger(__name__)


def test_successful_login_and_session_creation():
    """Test Case TC-POS-001: Successful login and session creation.
    
    This test verifies that a user can successfully login with valid credentials
    and a user session is created.
    """
    driver = get_driver()
    
    try:
        # Test data
        login_url = "https://ecommerce.example.com/login"
        valid_email = "testuser@example.com"
        valid_password = "Test@1234"
        
        # Navigate to login page
        driver.get(login_url)
        logger.info(f"Navigated to login page: {login_url}")
        
        # Enter email
        email_input = driver.find_element("id", "email")
        email_input.clear()
        email_input.send_keys(valid_email)
        logger.info(f"Entered email: {valid_email}")
        
        # Enter password
        password_input = driver.find_element("id", "password")
        password_input.clear()
        password_input.send_keys(valid_password)
        logger.info("Entered password")
        
        # Click login button
        login_button = driver.find_element("id", "loginButton")
        login_button.click()
        logger.info("Clicked login button")
        
        # Assertion: Validate login success
        success_indicator = driver.find_element("css selector", ".success-message")
        assert success_indicator.is_displayed(), "Login success message should be displayed"
        logger.info("Login success validated")
        
        # Assertion: Validate user session created
        user_profile = driver.find_element("id", "userProfile")
        assert user_profile.is_displayed(), "User session should be created and profile visible"
        logger.info("User session creation validated")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()


def test_login_with_invalid_username():
    """Test Case TC_LOGIN_006: Login with invalid username.
    
    This test verifies that attempting to login with an invalid username
    displays appropriate error message and user remains on login page.
    """
    driver = get_driver()
    
    try:
        # Test data
        login_url = "https://ecommerce-website.com/login"
        invalid_email = "invaliduser@example.com"
        valid_password = "ValidPass123!"
        
        # Navigate to login page
        driver.get(login_url)
        logger.info(f"Navigated to login page: {login_url}")
        
        # Enter invalid email
        email_input = driver.find_element("id", "email")
        email_input.clear()
        email_input.send_keys(invalid_email)
        logger.info(f"Entered invalid email: {invalid_email}")
        
        # Enter password
        password_input = driver.find_element("id", "password")
        password_input.clear()
        password_input.send_keys(valid_password)
        logger.info("Entered password")
        
        # Click login button
        login_button = driver.find_element("id", "loginButton")
        login_button.click()
        logger.info("Clicked login button")
        
        # Assertion: Validate login failure
        error_message = driver.find_element("css selector", ".error-message")
        assert error_message.is_displayed(), "Error message should be displayed for invalid credentials"
        logger.info("Login failure validated")
        
        # Assertion: Validate user remains on login page
        login_form = driver.find_element("id", "loginForm")
        assert login_form.is_displayed(), "User should remain on login page after failed login"
        assert "login" in driver.current_url.lower(), "URL should still contain 'login'"
        logger.info("User remains on login page validated")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()