from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_blank_username_validation():
    """
    Test Case TC_LOGIN_008: Verify validation error when username is blank
    
    Steps:
    1. Navigate to login page
    2. Leave username field blank
    3. Enter valid password
    4. Click login button
    5. Verify validation error is displayed
    6. Verify login is prevented
    """
    driver = get_driver()
    login_page = LoginPage()
    
    try:
        # Step 1: Navigate to login page
        login_page.navigate_to_login_page(driver)
        
        # Step 2: Enter blank username (skip entering username)
        # Username field remains blank
        
        # Step 3: Enter password
        login_page.enter_password(driver, "ValidPass123!")
        
        # Step 4: Click login button
        login_page.click_login_button(driver)
        
        # Step 5: Verify validation error is displayed
        assert login_page.verify_validation_error(driver), "Validation error should be displayed for blank username"
        
        # Step 6: Verify login is prevented
        assert login_page.verify_login_prevented(driver), "Login should be prevented when username is blank"
        
    finally:
        driver.quit()


def test_login_account_lockout_after_multiple_failed_attempts():
    """
    Test Case TC_LOGIN_010: Verify account lockout after 5 failed login attempts
    
    Steps:
    1. Navigate to login page
    2. Enter valid username
    3. Attempt login with 5 different wrong passwords
    4. Attempt login with correct password (should be locked)
    5. Verify account lockout message is displayed
    6. Verify email notification is sent
    """
    driver = get_driver()
    login_page = LoginPage()
    
    try:
        # Step 1: Navigate to login page
        login_page.navigate_to_login_page(driver)
        
        # Step 2: Enter valid username
        login_page.enter_username(driver, "validuser@example.com")
        
        # Step 3: Attempt login with 5 wrong passwords
        failed_attempts = [
            "WrongPass1",
            "WrongPass2",
            "WrongPass3",
            "WrongPass4",
            "WrongPass5"
        ]
        
        for wrong_password in failed_attempts:
            login_page.enter_password(driver, wrong_password)
            login_page.click_login_button(driver)
            # Each attempt should fail
            # Note: In real scenario, you might need to clear password field between attempts
        
        # Step 4: Attempt login with correct password (account should be locked)
        login_page.enter_password(driver, "ValidPass123!")
        login_page.click_login_button(driver)
        
        # Step 5: Verify account lockout message is displayed
        assert login_page.verify_account_lockout_message(driver), "Account lockout message should be displayed after 5 failed attempts"
        
        # Step 6: Verify email notification is sent
        assert login_page.verify_email_notification_sent(driver), "Email notification should be sent for account lockout"
        
    finally:
        driver.quit()
