# core/selenium_wrapper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import yaml
import os


def load_config():
    """
    Load configuration from config.yaml file
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


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
        timeout = config.get('ui', {}).get('explicit_wait', 20)
    
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
        timeout = config.get('ui', {}).get('explicit_wait', 20)
    
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
        timeout = config.get('ui', {}).get('explicit_wait', 20)
    
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return True
    except TimeoutException:
        return False


def wait_for_element_to_disappear(driver, locator, timeout=None):
    """
    Wait for element to disappear from DOM
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
    
    Returns:
        bool: True if element disappeared, False otherwise
    """
    if timeout is None:
        config = load_config()
        timeout = config.get('ui', {}).get('explicit_wait', 20)
    
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located(locator)
        )
        return True
    except TimeoutException:
        return False