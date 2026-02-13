"""Selenium Wrapper Module

Provides reusable wrapper methods for common Selenium operations.
Includes explicit waits, element interactions, and error handling.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging


logger = logging.getLogger(__name__)


class SeleniumWrapper:
    """Wrapper class for Selenium WebDriver operations"""
    
    def __init__(self, driver, timeout=10):
        """
        Args:
            driver: Selenium WebDriver instance
            timeout (int): Default timeout for waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Optional custom timeout
        
        Returns:
            WebElement: The found element
        """
        wait_time = timeout if timeout else self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Optional custom timeout
        
        Returns:
            WebElement: The visible element
        """
        wait_time = timeout if timeout else self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Optional custom timeout
        
        Returns:
            WebElement: The clickable element
        """
        wait_time = timeout if timeout else self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.info(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {wait_time} seconds: {locator}")
            raise
    
    def click_element(self, locator):
        """Click on an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        element = self.wait_for_element_clickable(locator)
        element.click()
        logger.info(f"Clicked element: {locator}")
    
    def enter_text(self, locator, text):
        """Enter text into an input field
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to enter
        """
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Entered text into element: {locator}")
    
    def get_text(self, locator):
        """Get text from an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator)
        text = element.text
        logger.info(f"Got text from element: {locator} - Text: {text}")
        return text
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False
