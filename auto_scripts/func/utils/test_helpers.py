"""Test Helper Utilities for Login Test Suite"""

import time
import os
from datetime import datetime


def wait_for_lockout_period(seconds=1800):
    """Wait for account lockout period to expire
    
    Args:
        seconds (int): Number of seconds to wait (default: 1800 = 30 minutes)
    """
    print(f"Waiting for lockout period: {seconds} seconds ({seconds/60} minutes)")
    time.sleep(seconds)


def generate_timestamp():
    """Generate timestamp string for logging and reporting
    
    Returns:
        str: Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def take_screenshot(driver, test_name, screenshot_dir="screenshots"):
    """Take screenshot and save with test name and timestamp
    
    Args:
        driver (WebDriver): WebDriver instance
        test_name (str): Name of the test
        screenshot_dir (str): Directory to save screenshots
    
    Returns:
        str: Path to saved screenshot
    """
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)
    
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")
    return filepath


def log_test_step(step_number, description, status="INFO"):
    """Log test step with timestamp
    
    Args:
        step_number (int): Step number
        description (str): Step description
        status (str): Status (INFO, PASS, FAIL, WARNING)
    """
    timestamp = generate_timestamp()
    print(f"[{timestamp}] [{status}] Step {step_number}: {description}")


def retry_action(action_func, max_retries=3, delay=1):
    """Retry an action multiple times with delay
    
    Args:
        action_func (callable): Function to retry
        max_retries (int): Maximum number of retries
        delay (int): Delay between retries in seconds
    
    Returns:
        Result of action_func if successful
    
    Raises:
        Exception: Last exception if all retries fail
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return action_func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"All {max_retries} attempts failed.")
    
    raise last_exception


def validate_error_message(actual_message, expected_keywords):
    """Validate that error message contains expected keywords
    
    Args:
        actual_message (str): Actual error message displayed
        expected_keywords (list): List of keywords that should be in the message
    
    Returns:
        bool: True if all keywords are found, False otherwise
    """
    actual_lower = actual_message.lower()
    return all(keyword.lower() in actual_lower for keyword in expected_keywords)