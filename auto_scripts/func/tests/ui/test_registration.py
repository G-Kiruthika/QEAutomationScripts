"""Registration Test Suite

This module contains test cases for user registration functionality.
Follows the Python UI & API Automation Framework standards.
"""

import pytest
import logging
from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver

logger = logging.getLogger(__name__)


def test_register_new_user():
    """Test successful registration of a new user.
    
    This test verifies that a new user can successfully register
    with valid credentials and receives a success message.
    """
    driver = get_driver()
    try:
        registration_page = RegistrationPage(driver)
        
        # Test data
        first_name = "John"
        last_name = "Doe"
        email = "john.doe@example.com"
        password = "Password123"
        
        # Execute registration flow
        registration_page.enter_first_name(first_name)
        registration_page.enter_last_name(last_name)
        registration_page.enter_email(email)
        registration_page.enter_password(password)
        registration_page.click_register_button()
        
        # Verify success message
        success_message = registration_page.get_success_message()
        assert success_message is not None, "Success message should be displayed"
        logger.info(f"Registration successful for user: {email}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()


def test_register_duplicate_email():
    """Test registration with duplicate email address.
    
    This test verifies that attempting to register with an already
    registered email address displays an appropriate error message.
    """
    driver = get_driver()
    try:
        registration_page = RegistrationPage(driver)
        
        # Test data
        first_name = "Jane"
        last_name = "Doe"
        email = "john.doe@example.com"
        password = "Password123"
        
        # Execute registration flow
        registration_page.enter_first_name(first_name)
        registration_page.enter_last_name(last_name)
        registration_page.enter_email(email)
        registration_page.enter_password(password)
        registration_page.click_register_button()
        
        # Verify error message
        error_message = registration_page.get_error_message()
        assert error_message is not None, "Error message for duplicate email should be displayed"
        logger.info(f"Duplicate email validation successful for: {email}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()
