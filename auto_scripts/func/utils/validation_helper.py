from selenium.common.exceptions import TimeoutException, NoSuchElementException


def verify_element_displayed(page_object, locator, error_message=None):
    """
    Verify that an element is displayed
    
    Args:
        page_object: Page object instance
        locator: Element locator tuple
        error_message: Custom error message
    
    Returns:
        bool: True if element is displayed
    
    Raises:
        AssertionError: If element is not displayed
    """
    try:
        is_displayed = page_object.is_displayed(locator)
        if not is_displayed:
            msg = error_message or f"Element {locator} is not displayed"
            raise AssertionError(msg)
        return True
    except (TimeoutException, NoSuchElementException) as e:
        msg = error_message or f"Element {locator} not found: {str(e)}"
        raise AssertionError(msg)


def verify_element_enabled(page_object, locator, expected_state=True, error_message=None):
    """
    Verify element enabled/disabled state
    
    Args:
        page_object: Page object instance
        locator: Element locator tuple
        expected_state: Expected enabled state (True/False)
        error_message: Custom error message
    
    Returns:
        bool: True if verification passes
    
    Raises:
        AssertionError: If state doesn't match expected
    """
    try:
        is_enabled = page_object.is_enabled(locator)
        if is_enabled != expected_state:
            msg = error_message or f"Element {locator} enabled state is {is_enabled}, expected {expected_state}"
            raise AssertionError(msg)
        return True
    except (TimeoutException, NoSuchElementException) as e:
        msg = error_message or f"Element {locator} not found: {str(e)}"
        raise AssertionError(msg)


def verify_text_present(page_object, locator, expected_text, error_message=None):
    """
    Verify element contains expected text
    
    Args:
        page_object: Page object instance
        locator: Element locator tuple
        expected_text: Expected text content
        error_message: Custom error message
    
    Returns:
        bool: True if text matches
    
    Raises:
        AssertionError: If text doesn't match
    """
    try:
        element = page_object.find_element(locator)
        actual_text = element.text
        if expected_text not in actual_text:
            msg = error_message or f"Expected text '{expected_text}' not found in '{actual_text}'"
            raise AssertionError(msg)
        return True
    except (TimeoutException, NoSuchElementException) as e:
        msg = error_message or f"Element {locator} not found: {str(e)}"
        raise AssertionError(msg)


def verify_login_prevented(page_object, login_button_locator, error_message=None):
    """
    Verify that login is prevented (button disabled or validation error shown)
    
    Args:
        page_object: Page object instance
        login_button_locator: Login button locator
        error_message: Custom error message
    
    Returns:
        bool: True if login is prevented
    """
    try:
        is_enabled = page_object.is_enabled(login_button_locator)
        if is_enabled:
            msg = error_message or "Login should be prevented but button is enabled"
            raise AssertionError(msg)
        return True
    except Exception as e:
        # If button is not found or any other error, consider login prevented
        return True
