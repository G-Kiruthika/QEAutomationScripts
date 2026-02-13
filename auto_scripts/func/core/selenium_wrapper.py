# core/selenium_wrapper.py

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
        WebElement: The located element
    """
    if timeout is None:
        config = load_config()
        timeout = config.get('browser', {}).get('explicit_wait', 20)
    
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        raise TimeoutException(f"Element {locator} not found within {timeout} seconds")


def wait_for_element_clickable(driver, locator, timeout=None):
    """
    Wait for element to be clickable
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    
    Returns:
        WebElement: The clickable element
    """
    if timeout is None:
        config = load_config()
        timeout = config.get('browser', {}).get('explicit_wait', 20)
    
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except TimeoutException:
        raise TimeoutException(f"Element {locator} not clickable within {timeout} seconds")


def click_element(driver, locator, timeout=None):
    """
    Wait for element and click it
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    """
    element = wait_for_element_clickable(driver, locator, timeout)
    element.click()


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


def get_text(driver, locator, timeout=None):
    """
    Wait for element and get its text
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    
    Returns:
        str: Element text
    """
    element = wait_for_element(driver, locator, timeout)
    return element.text


def is_element_visible(driver, locator, timeout=5):
    """
    Check if element is visible
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    
    Returns:
        bool: True if element is visible, False otherwise
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return True
    except (TimeoutException, NoSuchElementException):
        return False


def is_element_present(driver, locator, timeout=5):
    """
    Check if element is present in DOM
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    
    Returns:
        bool: True if element is present, False otherwise
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return True
    except (TimeoutException, NoSuchElementException):
        return False
