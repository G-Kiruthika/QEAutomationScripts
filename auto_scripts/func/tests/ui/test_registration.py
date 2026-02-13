"""UI Test Suite for User Registration Functionality"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
import logging
from core.driver_factory import get_driver
from pages.registration_page import RegistrationPage

# Configure logging
logger = logging.getLogger(__name__)


def test_register_new_user():
    """Test successful registration of a new user"""
    driver = get_driver()
    try:
        registration_page = RegistrationPage(driver)
        
        # Test data
        first_name = "John"
        last_name = "Doe"
        email = "john.doe@example.com"
        password = "Password123"
        
        # Execute test flow
        registration_page.enter_first_name(first_name)
        registration_page.enter_last_name(last_name)
        registration_page.enter_email(email)
        registration_page.enter_password(password)
        registration_page.click_register_button()
        success_message = registration_page.get_success_message()
        
        # Assertion
        assert success_message is not None, "Success message should be displayed"
        assert len(success_message) > 0, "Success message should not be empty"
        logger.info(f"Test passed: New user registered successfully with message: {success_message}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()


def test_register_duplicate_email():
    """Test registration with duplicate email address"""
    driver = get_driver()
    try:
        registration_page = RegistrationPage(driver)
        
        # Test data
        first_name = "Jane"
        last_name = "Doe"
        email = "john.doe@example.com"
        password = "Password123"
        
        # Execute test flow
        registration_page.enter_first_name(first_name)
        registration_page.enter_last_name(last_name)
        registration_page.enter_email(email)
        registration_page.enter_password(password)
        registration_page.click_register_button()
        error_message = registration_page.get_error_message()
        
        # Assertion
        assert error_message is not None, "Error message should be displayed for duplicate email"
        assert len(error_message) > 0, "Error message should not be empty"
        logger.info(f"Test passed: Duplicate email validation working with message: {error_message}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()
