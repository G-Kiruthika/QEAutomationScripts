# Existing imports and test methods
from LoginPage import LoginPage
import pytest

# ... existing test methods ...

# TC_LOGIN_007: Test navigation to login page, click 'Forgot Password', verify redirect and presence of email input and instructions.
def test_TC_LOGIN_007_forgot_password_navigation_and_validation(driver):
    login_page = LoginPage(driver)
    login_page.navigate('https://example.com/login')
    login_page.click_forgot_password()
    assert login_page.is_on_forgot_password_page('https://example.com/forgot-password'), "Did not redirect to Forgot Password page"
    email_input_present = driver.find_element_by_id('email') is not None
    instructions_present = driver.find_element_by_xpath("//*[contains(text(), 'Please enter your email address')]") is not None
    assert email_input_present, "Email input not present on Forgot Password page"
    assert instructions_present, "Instructions not present on Forgot Password page"

# TC_LOGIN_008: Test maximum length email input, valid password entry, click login, assert login or error.
def test_TC_LOGIN_008_max_length_email_and_valid_password(driver):
    login_page = LoginPage(driver)
    login_page.navigate('https://example.com/login')
    max_length_email = 'a' * 64 + '@example.com'  # adjust as per system max
    valid_password = 'ValidPassword123!'
    login_page.enter_username(max_length_email)
    login_page.enter_password(valid_password)
    login_page.click_login()
    # Check for either successful login or error message
    try:
        # Example: successful login redirects to dashboard
        assert driver.current_url == 'https://example.com/dashboard', "Did not login successfully with max length email"
    except AssertionError:
        error_msg = login_page.get_error_message()
        assert error_msg is not None and error_msg != '', "No error message shown for max length email login failure"

# TC_LOGIN_009: Test minimum allowed length login, valid password, and successful login/error handling.
def test_TC_LOGIN_009_min_length_login_and_valid_password(driver):
    login_page = LoginPage(driver)
    login_page.navigate('https://example.com/login')
    min_length_username = 'a@b.co'  # adjust as per system minimum
    valid_password = 'ValidPassword123!'
    login_page.enter_username(min_length_username)
    login_page.enter_password(valid_password)
    login_page.click_login()
    # Check for either successful login or error message
    try:
        assert driver.current_url == 'https://example.com/dashboard', "Did not login successfully with min length username"
    except AssertionError:
        error_msg = login_page.get_error_message()
        assert error_msg is not None and error_msg != '', "No error message shown for min length username login failure"

# TC_LOGIN_010: Test valid email, incorrect password, repeated failed attempts, error messages, and lockout/CAPTCHA detection.
def test_TC_LOGIN_010_valid_email_incorrect_password_lockout(driver):
    login_page = LoginPage(driver)
    login_page.navigate('https://example.com/login')
    valid_email = 'user@example.com'
    invalid_password = 'WrongPassword!'
    max_attempts = 3  # adjust as per system lockout policy
    lockout_detected = False
    for attempt in range(1, max_attempts + 1):
        login_page.enter_username(valid_email)
        login_page.enter_password(invalid_password)
        login_page.click_login()
        error_msg = login_page.get_error_message()
        assert error_msg is not None and error_msg != '', f"No error message shown for failed login attempt {attempt}"
        # Check for CAPTCHA or lockout after last attempt
        if attempt == max_attempts:
            if login_page.is_captcha_present():
                lockout_detected = True
            elif login_page.is_account_locked():
                lockout_detected = True
            else:
                lockout_detected = False
    assert lockout_detected, "Account was not locked or CAPTCHA not shown after repeated failed attempts"
