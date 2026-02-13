from selenium.webdriver.common.by import By
import pytest
from core.driver_factory import get_driver
from pages.login_page import LoginPage
from utils.error_handling import log_error
from utils.email_notification import verify_email_sent


def test_login_account_lockout_after_multiple_failures():
    """TC_LOGIN_010: Verify account lockout after 5 consecutive failed login attempts"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.navigate_to_login("https://ecommerce-website.com/login")
    
    # Enter valid username
    username = "validuser@example.com"
    incorrect_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    
    # Attempt login with 5 incorrect passwords
    for wrong_password in incorrect_passwords:
        login_page.enter_email(username)
        login_page.enter_password_xpath(wrong_password)
        login_page.click_login_xpath()
    
    # Attempt login with correct password after lockout
    login_page.enter_email(username)
    login_page.enter_password_xpath("ValidPass123!")
    login_page.click_login_xpath()
    
    # Get account lockout message
    lockout_error = login_page.verify_login_failure()
    assert lockout_error, "Account lockout message not displayed after 5 failed attempts"
    
    # Verify email notification sent
    email_sent = verify_email_sent(username)
    assert email_sent, "Email notification not sent for account lockout"
    
    driver.quit()