"""Base Page Module

This module provides the BasePage class that serves as the foundation
for all Page Object classes in the framework.
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects.
    
    This class provides common methods and utilities that can be used
    across all page objects in the framework.
    """
    
    def __init__(self, driver, timeout=10):
        """Initialize BasePage.
        
        Args:
            driver (WebDriver): Selenium WebDriver instance
            timeout (int): Default timeout for wait operations
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def find_element(self, locator, timeout=None):
        """Find an element on the page.
        
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
            logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements on the page.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            list: List of WebElements
        """
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            elements = self.driver.find_elements(*locator)
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.warning(f"No elements found: {locator}")
            return []
    
    def click_element(self, locator, timeout=None):
        """Click on an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info(f"Clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to click element {locator}: {str(e)}")
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
            element = self.find_element(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Entered text into element: {locator}")
        except Exception as e:
            logger.error(f"Failed to enter text into element {locator}: {str(e)}")
            raise
    
    def get_element_text(self, locator, timeout=None):
        """Get text from an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            str: Element text
        """
        try:
            element = self.find_element(locator, timeout)
            text = element.text
            logger.debug(f"Retrieved text from element: {locator}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator, timeout=None):
        """Check if an element is visible on the page.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to 5 seconds.
        
        Returns:
            bool: True if element is visible, False otherwise
        """
        wait_time = timeout or 5
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=None):
        """Check if an element is present in the DOM.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to 5 seconds.
        
        Returns:
            bool: True if element is present, False otherwise
        """
        wait_time = timeout or 5
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for an element to disappear from the page.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        
        Returns:
            bool: True if element disappeared, False otherwise
        """
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located(locator)
            )
            logger.debug(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element still visible after {wait_time} seconds: {locator}")
            return False
    
    def get_page_title(self):
        """Get the current page title.
        
        Returns:
            str: Page title
        """
        return self.driver.title
    
    def get_current_url(self):
        """Get the current page URL.
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def navigate_to(self, url):
        """Navigate to a specific URL.
        
        Args:
            url (str): URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def refresh_page(self):
        """Refresh the current page."""
        logger.info("Refreshing page")
        self.driver.refresh()
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to an element on the page.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int, optional): Custom timeout. Defaults to instance timeout.
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.debug(f"Scrolled to element: {locator}")
    
    def take_screenshot(self, filename):
        """Take a screenshot and save it to a file.
        
        Args:
            filename (str): Path to save the screenshot
        
        Returns:
            bool: True if screenshot was saved successfully
        """
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save screenshot: {str(e)}")
            return False
