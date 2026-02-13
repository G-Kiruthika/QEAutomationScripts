# utils/screenshot_helper.py

import os
from datetime import datetime


def take_screenshot(driver, test_name, screenshot_dir='screenshots'):
    """Take screenshot and save with timestamp
    
    Args:
        driver: WebDriver instance
        test_name (str): Name of the test
        screenshot_dir (str): Directory to save screenshots
    
    Returns:
        str: Path to saved screenshot
    """
    # Create screenshots directory if it doesn't exist
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{test_name}_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)
    
    # Take and save screenshot
    driver.save_screenshot(filepath)
    
    return filepath


def take_screenshot_on_failure(driver, test_name):
    """Take screenshot on test failure
    
    Args:
        driver: WebDriver instance
        test_name (str): Name of the failed test
    
    Returns:
        str: Path to saved screenshot
    """
    screenshot_dir = 'screenshots/failures'
    return take_screenshot(driver, f"FAILED_{test_name}", screenshot_dir)
