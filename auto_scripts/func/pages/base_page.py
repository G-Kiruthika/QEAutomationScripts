"""Base Page Module

This module provides the base page class that all page objects should inherit from.
Contains common methods and utilities for page interactions.
"""

from core.selenium_wrapper import SeleniumWrapper


class BasePage:
    """Base class for all page objects
    
    Provides common functionality for page interactions using Selenium wrapper.
    All page classes should inherit from this base class.
    """

    def __init__(self, driver, timeout=10):
        """Initialize BasePage
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for operations in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wrapper = SeleniumWrapper(driver, timeout)

    def find_element(self, locator, timeout=None):
        """Find element using locator
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            WebElement: Found element
        """
        return self.wrapper.find_element(locator, timeout)

    def find_elements(self, locator, timeout=None):
        """Find multiple elements using locator
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            list: List of found WebElements
        """
        return self.wrapper.find_elements(locator, timeout)

    def click_element(self, locator, timeout=None):
        """Click element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if click successful
        """
        return self.wrapper.click_element(locator, timeout)

    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """Enter text into input field
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to enter
            clear_first (bool): Whether to clear field before entering text
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if text entry successful
        """
        return self.wrapper.enter_text(locator, text, clear_first, timeout)

    def get_text(self, locator, timeout=None):
        """Get text from element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            str: Element text
        """
        return self.wrapper.get_text(locator, timeout)

    def get_attribute(self, locator, attribute_name, timeout=None):
        """Get attribute value from element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            attribute_name (str): Name of attribute to retrieve
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            str: Attribute value
        """
        return self.wrapper.get_attribute(locator, attribute_name, timeout)

    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if element is visible
        """
        return self.wrapper.is_element_visible(locator, timeout)

    def is_element_present(self, locator, timeout=None):
        """Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if element is present
        """
        return self.wrapper.is_element_present(locator, timeout)

    def is_element_clickable(self, locator, timeout=None):
        """Check if element is clickable
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if element is clickable
        """
        return self.wrapper.is_element_clickable(locator, timeout)

    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear from DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if element disappeared
        """
        return self.wrapper.wait_for_element_to_disappear(locator, timeout)

    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if scroll successful
        """
        return self.wrapper.scroll_to_element(locator, timeout)

    def hover_over_element(self, locator, timeout=None):
        """Hover mouse over element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if hover successful
        """
        return self.wrapper.hover_over_element(locator, timeout)

    def select_dropdown_by_text(self, locator, text, timeout=None):
        """Select dropdown option by visible text
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Visible text of option to select
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if selection successful
        """
        return self.wrapper.select_dropdown_by_text(locator, text, timeout)

    def switch_to_frame(self, locator, timeout=None):
        """Switch to iframe
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if switch successful
        """
        return self.wrapper.switch_to_frame(locator, timeout)

    def switch_to_default_content(self):
        """Switch back to default content from iframe
        
        Returns:
            bool: True if switch successful
        """
        return self.wrapper.switch_to_default_content()

    def take_screenshot(self, filepath):
        """Take screenshot and save to file
        
        Args:
            filepath (str): Path where screenshot should be saved
            
        Returns:
            bool: True if screenshot saved successfully
        """
        return self.wrapper.take_screenshot(filepath)

    def execute_javascript(self, script, *args):
        """Execute JavaScript code
        
        Args:
            script (str): JavaScript code to execute
            *args: Arguments to pass to the script
            
        Returns:
            Any: Result of JavaScript execution
        """
        return self.wrapper.execute_javascript(script, *args)

    def get_current_url(self):
        """Get current page URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url

    def get_page_title(self):
        """Get page title
        
        Returns:
            str: Page title
        """
        return self.driver.title

    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()

    def navigate_back(self):
        """Navigate back in browser history"""
        self.driver.back()

    def navigate_forward(self):
        """Navigate forward in browser history"""
        self.driver.forward()
