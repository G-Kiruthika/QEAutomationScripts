"""Wait utility functions for Selenium WebDriver.

Provides reusable wait methods for common scenarios in test automation.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from auto_scripts.api.utils.logger import logger


class WaitUtils:
    """Utility class for WebDriver wait operations."""
    
    def __init__(self, driver, timeout=20):
        """Initialize WaitUtils with driver and default timeout.
        
        Args:
            driver: Selenium WebDriver instance
            timeout (int): Default timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible.
        
        Args:
            locator (tuple): Element locator (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: The visible element
        
        Raises:
            TimeoutException: If element not visible within timeout
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Element {locator} is visible")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not visible within {wait_time} seconds")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: The clickable element
        
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.info(f"Element {locator} is clickable")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not clickable within {wait_time} seconds")
            raise
    
    def wait_for_element_presence(self, locator, timeout=None):
        """Wait for element to be present in DOM.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: The present element
        
        Raises:
            TimeoutException: If element not present within timeout
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Element {locator} is present in DOM")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not present within {wait_time} seconds")
            raise
    
    def wait_for_text_in_element(self, locator, text, timeout=None):
        """Wait for specific text to appear in element.
        
        Args:
            locator (tuple): Element locator
            text (str): Expected text
            timeout (int): Custom timeout (optional)
        
        Returns:
            bool: True if text found
        
        Raises:
            TimeoutException: If text not found within timeout
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            result = wait.until(EC.text_to_be_present_in_element(locator, text))
            logger.info(f"Text '{text}' found in element {locator}")
            return result
        except TimeoutException:
            logger.error(f"Text '{text}' not found in element {locator} within {wait_time} seconds")
            raise
    
    def wait_for_element_invisible(self, locator, timeout=None):
        """Wait for element to become invisible.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout (optional)
        
        Returns:
            bool: True if element invisible
        
        Raises:
            TimeoutException: If element still visible after timeout
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            result = wait.until(EC.invisibility_of_element_located(locator))
            logger.info(f"Element {locator} is invisible")
            return result
        except TimeoutException:
            logger.error(f"Element {locator} still visible after {wait_time} seconds")
            raise
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """Wait for URL to contain specific fragment.
        
        Args:
            url_fragment (str): Expected URL fragment
            timeout (int): Custom timeout (optional)
        
        Returns:
            bool: True if URL contains fragment
        
        Raises:
            TimeoutException: If URL doesn't contain fragment within timeout
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            result = wait.until(EC.url_contains(url_fragment))
            logger.info(f"URL contains '{url_fragment}'")
            return result
        except TimeoutException:
            logger.error(f"URL does not contain '{url_fragment}' within {wait_time} seconds")
            raise
