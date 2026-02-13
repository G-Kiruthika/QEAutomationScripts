from core.driver_factory import get_driver
from pages.login_page import LoginPage
import pytest

def test_login_empty_username():
    """TC_LOGIN_008: Test login with empty username and valid password"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.navigate_to_login()
    
    # Enter empty username
    login_page.enter_email("")
    
    # Enter valid password
    login_page.enter_password("ValidPass123!")
    
    # Click login button
    login_page.click_login()
    
    # Verify login is prevented (user remains on login page)
    assert login_page.verify_remain_on_login(), "Expected to remain on login page with empty username"
    
    driver.quit()

def test_login_multiple_failed_attempts_lockout():
    """TC_LOGIN_010: Test account lockout after multiple failed login attempts"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.navigate_to_login()
    
    # Enter valid username
    login_page.enter_email("validuser@example.com")
    
    # Attempt 1: Wrong password
    login_page.enter_password("WrongPass1")
    login_page.click_login()
    
    # Attempt 2: Wrong password
    login_page.enter_password("WrongPass2")
    login_page.click_login()
    
    # Attempt 3: Wrong password
    login_page.enter_password("WrongPass3")
    login_page.click_login()
    
    # Attempt 4: Wrong password
    login_page.enter_password("WrongPass4")
    login_page.click_login()
    
    # Attempt 5: Wrong password
    login_page.enter_password("WrongPass5")
    login_page.click_login()
    
    # Attempt 6: Correct password (should be locked out)
    login_page.enter_password("ValidPass123!")
    login_page.click_login()
    
    # Verify login failure due to account lockout
    assert login_page.verify_login_failure(), "Expected login failure message due to account lockout"
    
    # Verify user remains on login page
    assert login_page.verify_remain_on_login(), "Expected to remain on login page after lockout"
    
    driver.quit()
