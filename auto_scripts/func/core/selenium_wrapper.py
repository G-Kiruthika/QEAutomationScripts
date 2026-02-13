from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import yaml
import os


def load_config():
    """
    Load configuration from config.yaml
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def wait_for_element(driver, locator, timeout=None):
    """
    Wait for element to be present and visible
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    
    Returns:
        WebElement: The found element
    """
    if timeout is None:
        config = load_config()
        timeout = config.get('timeouts', {}).get('element_wait', 10)
    
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        raise TimeoutException(f"Element {locator} not found within {timeout} seconds")


def click_element(driver, locator, timeout=None):
    """
    Wait for element to be clickable and click it
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    """
    if timeout is None:
        config = load_config()
        timeout = config.get('timeouts', {}).get('element_wait', 10)
    
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    except TimeoutException:
        raise TimeoutException(f"Element {locator} not clickable within {timeout} seconds")


def enter_text(driver, locator, text, timeout=None):
    """
    Wait for element and enter text
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        text: Text to enter
        timeout: Maximum wait time in seconds
    """
    element = wait_for_element(driver, locator, timeout)
    element.clear()
    element.send_keys(text)


def is_element_visible(driver, locator, timeout=None):
    """
    Check if element is visible
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    
    Returns:
        bool: True if element is visible, False otherwise
    """
    if timeout is None:
        config = load_config()
        timeout = config.get('timeouts', {}).get('element_wait', 10)
    
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return True
    except TimeoutException:
        return False


def is_element_enabled(driver, locator, timeout=None):
    """
    Check if element is enabled
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    
    Returns:
        bool: True if element is enabled, False otherwise
    """
    try:
        element = wait_for_element(driver, locator, timeout)
        return element.is_enabled()
    except (TimeoutException, NoSuchElementException):
        return False
