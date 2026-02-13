"""Selenium Wrapper Module

This module provides wrapper methods for common Selenium operations
with enhanced error handling and waiting mechanisms.
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)

logger = logging.getLogger(__name__)


class SeleniumWrapper:
    """Wrapper class for Selenium WebDriver operations."""
    
    def __init__(self, driver, timeout=10):
        """Initialize SeleniumWrapper.
        
        Args:
            driver (WebDriver): Selenium WebDriver instance
            timeout (int): Default timeout for wait operations
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present in DOM.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            WebElement: The located element
        
        Raises:
            TimeoutException: If element is not found within timeout
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            WebElement: The visible element
        
        Raises:
            TimeoutException: If element is not visible within timeout
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            WebElement: The clickable element
        
        Raises:
            TimeoutException: If element is not clickable within timeout
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            logger.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {wait_time} seconds: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """Click on an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Raises:
            ElementNotInteractableException: If element cannot be clicked
        """
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            element.click()
            logger.info(f"Clicked element: {locator}")
        except ElementNotInteractableException:
            logger.error(f"Element not interactable: {locator}")
            raise
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """Enter text into an input field.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            text (str): Text to enter
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
            clear_first (bool): Clear field before entering text. Defaults to True.
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Entered text '{text}' into element: {locator}")
        except Exception as e:
            logger.error(f"Failed to enter text into element {locator}: {str(e)}")
            raise
    
    def get_text(self, locator, timeout=None):
        """Get text from an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            str: Element text
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            text = element.text
            logger.debug(f"Retrieved text '{text}' from element: {locator}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout or 5)
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=None):
        """Check if element is present in DOM.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout or 5)
            return True
        except TimeoutException:
            return False
