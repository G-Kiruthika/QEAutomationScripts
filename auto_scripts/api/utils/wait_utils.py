# Wait utilities for automation framework
# Provides custom wait conditions and helpers

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class CustomWaitConditions:
    """Custom wait conditions for Selenium"""
    
    @staticmethod
    def element_has_text(locator, text):
        """Wait condition for element to have specific text
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
            text (str): Expected text
        
        Returns:
            function: Wait condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                return text in element.text
            except:
                return False
        return _predicate
    
    @staticmethod
    def element_attribute_contains(locator, attribute, value):
        """Wait condition for element attribute to contain value
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
            attribute (str): Attribute name
            value (str): Expected value
        
        Returns:
            function: Wait condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                attr_value = element.get_attribute(attribute)
                return value in attr_value if attr_value else False
            except:
                return False
        return _predicate
    
    @staticmethod
    def url_contains(url_fragment):
        """Wait condition for URL to contain fragment
        
        Args:
            url_fragment (str): URL fragment to check
        
        Returns:
            function: Wait condition function
        """
        def _predicate(driver):
            return url_fragment in driver.current_url
        return _predicate


def wait_for_condition(driver, condition, timeout=20, poll_frequency=0.5):
    """Wait for custom condition
    
    Args:
        driver: WebDriver instance
        condition: Wait condition function
        timeout (int): Maximum wait time in seconds
        poll_frequency (float): Polling interval in seconds
    
    Returns:
        bool: True if condition met, False otherwise
    """
    try:
        WebDriverWait(driver, timeout, poll_frequency).until(condition)
        return True
    except TimeoutException:
        return False


def wait_for_page_load(driver, timeout=30):
    """Wait for page to load completely
    
    Args:
        driver: WebDriver instance
        timeout (int): Maximum wait time in seconds
    
    Returns:
        bool: True if page loaded, False otherwise
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        return True
    except TimeoutException:
        return False


def wait_for_ajax(driver, timeout=20):
    """Wait for AJAX requests to complete (jQuery)
    
    Args:
        driver: WebDriver instance
        timeout (int): Maximum wait time in seconds
    
    Returns:
        bool: True if AJAX completed, False otherwise
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return jQuery.active == 0')
        )
        return True
    except:
        return False


def smart_wait(seconds):
    """Smart wait with logging
    
    Args:
        seconds (int/float): Wait time in seconds
    """
    time.sleep(seconds)
