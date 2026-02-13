"""Selenium wrapper module providing enhanced WebDriver interaction methods.

This module contains utility functions for common Selenium operations with
improved error handling and explicit waits.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
import time


class SeleniumWrapper:
    """
    Wrapper class providing enhanced Selenium WebDriver operations.
    """
    
    def __init__(self, driver, timeout=20):
        """
        Initialize SeleniumWrapper with a WebDriver instance.
        
        Args:
            driver (WebDriver): Selenium WebDriver instance
            timeout (int): Default explicit wait timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None, condition='presence'):
        """
        Wait for an element to meet a specific condition.
        
        Args:
            locator (tuple): Element locator (By.ID, 'element_id')
            timeout (int, optional): Wait timeout in seconds
            condition (str): Condition type ('presence', 'visible', 'clickable')
        
        Returns:
            WebElement: The located element
        
        Raises:
            TimeoutException: If element not found within timeout
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        
        try:
            if condition == 'presence':
                return wait.until(EC.presence_of_element_located(locator))
            elif condition == 'visible':
                return wait.until(EC.visibility_of_element_located(locator))
            elif condition == 'clickable':
                return wait.until(EC.element_to_be_clickable(locator))
            else:
                raise ValueError(f"Unknown condition: {condition}")
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not found with condition '{condition}' within {wait_timeout} seconds"
            )
    
    def click_element(self, locator, timeout=None):
        """
        Click an element after waiting for it to be clickable.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Wait timeout in seconds
        """
        element = self.wait_for_element(locator, timeout, condition='clickable')
        try:
            element.click()
        except ElementNotInteractableException:
            # Retry with JavaScript click
            self.driver.execute_script("arguments[0].click();", element)
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """
        Enter text into an input field.
        
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
            timeout (int, optional): Wait timeout in seconds
            clear_first (bool): Clear field before entering text
        """
        element = self.wait_for_element(locator, timeout, condition='visible')
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """
        Get text content of an element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Wait timeout in seconds
        
        Returns:
            str: Element text content
        """
        element = self.wait_for_element(locator, timeout, condition='visible')
        return element.text
    
    def is_element_present(self, locator, timeout=5):
        """
        Check if an element is present in the DOM.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout in seconds
        
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if an element is visible on the page.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout in seconds
        
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """
        Wait for URL to contain a specific fragment.
        
        Args:
            url_fragment (str): URL fragment to wait for
            timeout (int, optional): Wait timeout in seconds
        
        Returns:
            bool: True if URL contains fragment
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.url_contains(url_fragment))
    
    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll to an element to bring it into view.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Wait timeout in seconds
        """
        element = self.wait_for_element(locator, timeout, condition='presence')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Brief pause after scroll
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        """
        Get an attribute value from an element.
        
        Args:
            locator (tuple): Element locator
            attribute_name (str): Name of the attribute
            timeout (int, optional): Wait timeout in seconds
        
        Returns:
            str: Attribute value
        """
        element = self.wait_for_element(locator, timeout, condition='presence')
        return element.get_attribute(attribute_name)
    
    def switch_to_frame(self, frame_locator, timeout=None):
        """
        Switch to an iframe.
        
        Args:
            frame_locator (tuple): Frame element locator
            timeout (int, optional): Wait timeout in seconds
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        frame = wait.until(EC.frame_to_be_available_and_switch_to_it(frame_locator))
        return frame
    
    def switch_to_default_content(self):
        """
        Switch back to the main document from an iframe.
        """
        self.driver.switch_to.default_content()