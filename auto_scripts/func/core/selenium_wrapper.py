"""Selenium Wrapper Module for common WebDriver operations"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import yaml
import os


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def wait_for_element(driver, locator, timeout=None):
    """Wait for element to be present and visible
    
    Args:
        driver (WebDriver): WebDriver instance
        locator (tuple): Locator tuple (By.*, value)
        timeout (int): Wait timeout in seconds
    
    Returns:
        WebElement: Found element
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


def wait_for_element_clickable(driver, locator, timeout=None):
    """Wait for element to be clickable
    
    Args:
        driver (WebDriver): WebDriver instance
        locator (tuple): Locator tuple (By.*, value)
        timeout (int): Wait timeout in seconds
    
    Returns:
        WebElement: Clickable element
    """
    if timeout is None:
        config = load_config()
        timeout = config.get('timeouts', {}).get('element_wait', 10)
    
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except TimeoutException:
        raise TimeoutException(f"Element {locator} not clickable within {timeout} seconds")


def click_element(driver, locator, timeout=None):
    """Click on an element after waiting for it to be clickable
    
    Args:
        driver (WebDriver): WebDriver instance
        locator (tuple): Locator tuple (By.*, value)
        timeout (int): Wait timeout in seconds
    """
    element = wait_for_element_clickable(driver, locator, timeout)
    element.click()


def enter_text(driver, locator, text, timeout=None, clear_first=True):
    """Enter text into an input field
    
    Args:
        driver (WebDriver): WebDriver instance
        locator (tuple): Locator tuple (By.*, value)
        text (str): Text to enter
        timeout (int): Wait timeout in seconds
        clear_first (bool): Clear field before entering text
    """
    element = wait_for_element(driver, locator, timeout)
    if clear_first:
        element.clear()
    element.send_keys(text)


def is_element_visible(driver, locator, timeout=None):
    """Check if element is visible
    
    Args:
        driver (WebDriver): WebDriver instance
        locator (tuple): Locator tuple (By.*, value)
        timeout (int): Wait timeout in seconds
    
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


def is_element_present(driver, locator):
    """Check if element is present in DOM
    
    Args:
        driver (WebDriver): WebDriver instance
        locator (tuple): Locator tuple (By.*, value)
    
    Returns:
        bool: True if element is present, False otherwise
    """
    try:
        driver.find_element(*locator)
        return True
    except NoSuchElementException:
        return False


def get_element_text(driver, locator, timeout=None):
    """Get text from an element
    
    Args:
        driver (WebDriver): WebDriver instance
        locator (tuple): Locator tuple (By.*, value)
        timeout (int): Wait timeout in seconds
    
    Returns:
        str: Element text
    """
    element = wait_for_element(driver, locator, timeout)
    return element.text


def get_element_attribute(driver, locator, attribute, timeout=None):
    """Get attribute value from an element
    
    Args:
        driver (WebDriver): WebDriver instance
        locator (tuple): Locator tuple (By.*, value)
        attribute (str): Attribute name
        timeout (int): Wait timeout in seconds
    
    Returns:
        str: Attribute value
    """
    element = wait_for_element(driver, locator, timeout)
    return element.get_attribute(attribute)