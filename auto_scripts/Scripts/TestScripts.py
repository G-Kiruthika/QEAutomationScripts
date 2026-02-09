# TestScripts.py

# Test Case TC_LOGIN_001: Invalid login

def test_invalid_login(driver, login_page):
    """
    1. Navigate to the login screen.
    2. Enter an invalid username and/or password.
    3. Verify error message is displayed.
    """
    login_page.go_to_login()
    assert login_page.is_login_screen_displayed()
    login_page.enter_username('invalid_user')
    login_page.enter_password('invalid_pass')
    login_page.submit_login()
    assert login_page.error_message_displayed("Invalid username or password. Please try again.")

# Test Case TC_LOGIN_002: Check 'Remember Me' checkbox not present

def test_remember_me_checkbox_absent(driver, login_page):
    """
    1. Navigate to the login screen.
    2. Verify 'Remember Me' checkbox is not present.
    """
    login_page.go_to_login()
    assert login_page.is_login_screen_displayed()
    assert not login_page.is_remember_me_present()
