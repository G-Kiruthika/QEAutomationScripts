"""Selenium Wrapper Module

Provides enhanced wrapper methods for common Selenium operations
with built-in waits, error handling, and logging.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException
)
import logging

logger = logging.getLogger(__name__)


class SeleniumWrapper:
    """Enhanced Selenium wrapper with robust wait mechanisms."""
    
    def __init__(self, driver, timeout=10):
        """Initialize the wrapper.
        
        Args:
            driver (WebDriver): Selenium WebDriver instance
            timeout (int): Default timeout for waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None, condition='presence'):
        """Wait for element with specified condition.
        
        Args:
            locator (tuple): Element locator (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
            condition (str): Wait condition ('presence', 'visible', 'clickable')
        
        Returns:
            WebElement: Located element
        
        Raises:
            TimeoutException: If element not found within timeout
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        
        try:
            if condition == 'presence':
                element = wait.until(EC.presence_of_element_located(locator))
            elif condition == 'visible':
                element = wait.until(EC.visibility_of_element_located(locator))
            elif condition == 'clickable':
                element = wait.until(EC.element_to_be_clickable(locator))
            else:
                raise ValueError(f"Invalid condition: {condition}")
            
            logger.debug(f"Element found: {locator}")
            return element
            
        except TimeoutException:
            logger.error(f"Element not found within {timeout}s: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """Click on element with wait.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        """
        try:
            element = self.wait_for_element(locator, timeout, 'clickable')
            element.click()
            logger.info(f"Clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to click element {locator}: {str(e)}")
            raise
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """Enter text into element.
        
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
            timeout (int, optional): Custom timeout
            clear_first (bool): Clear field before entering text
        """
        try:
            element = self.wait_for_element(locator, timeout, 'visible')
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Entered text into element: {locator}")
        except Exception as e:
            logger.error(f"Failed to enter text into {locator}: {str(e)}")
            raise
    
    def get_element_text(self, locator, timeout=None):
        """Get text from element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        
        Returns:
            str: Element text
        """
        try:
            element = self.wait_for_element(locator, timeout, 'visible')
            text = element.text
            logger.debug(f"Retrieved text from {locator}: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout or 5, 'visible')
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=None):
        """Check if element is present in DOM.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout or 5, 'presence')
            return True
        except TimeoutException:
            return False
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from element.
        
        Args:
            locator (tuple): Element locator
            attribute (str): Attribute name
            timeout (int, optional): Custom timeout
        
        Returns:
            str: Attribute value
        """
        try:
            element = self.wait_for_element(locator, timeout, 'presence')
            value = element.get_attribute(attribute)
            logger.debug(f"Retrieved attribute '{attribute}' from {locator}: {value}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute from {locator}: {str(e)}")
            raise
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """Wait for URL to contain specified fragment.
        
        Args:
            url_fragment (str): URL fragment to wait for
            timeout (int, optional): Custom timeout
        
        Returns:
            bool: True if URL contains fragment
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.url_contains(url_fragment))
            logger.info(f"URL contains: {url_fragment}")
            return True
        except TimeoutException:
            logger.error(f"URL does not contain '{url_fragment}' within {timeout}s")
            return False
