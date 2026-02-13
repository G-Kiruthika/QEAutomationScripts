"""Base Page Module

Provides common page object functionality for all page classes.
Includes element interaction, waiting, and navigation methods.
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Base class for all page objects.
    
    Provides common methods for element interaction and page navigation.
    All page classes should inherit from this base class.
    """
    
    def __init__(self, driver, timeout=30):
        """Initialize BasePage with WebDriver instance.
        
        Args:
            driver (WebDriver): Selenium WebDriver instance
            timeout (int): Default timeout for waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, locator):
        """Find and return a single element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            WebElement: Found element
        """
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator):
        """Find and return multiple elements.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            list: List of WebElements
        """
        return self.driver.find_elements(*locator)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present in DOM.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout in seconds
        
        Returns:
            WebElement: Found element
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element: {locator}")
            raise
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout in seconds
        
        Returns:
            WebElement: Visible element
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element visibility: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout in seconds
        
        Returns:
            WebElement: Clickable element
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element to be clickable: {locator}")
            raise
    
    def click_element(self, locator):
        """Click on an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        element = self.wait_for_element_clickable(locator)
        element.click()
        self.logger.info(f"Clicked element: {locator}")
    
    def enter_text(self, locator, text):
        """Enter text into an input field.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to enter
        """
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Entered text '{text}' into element: {locator}")
    
    def get_element_text(self, locator):
        """Get text from an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator)
        text = element.text
        self.logger.info(f"Retrieved text '{text}' from element: {locator}")
        return text
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """Check if element is present in DOM.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False
    
    def get_page_title(self):
        """Get current page title.
        
        Returns:
            str: Page title
        """
        return self.driver.title
    
    def get_current_url(self):
        """Get current page URL.
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def navigate_to(self, url):
        """Navigate to a specific URL.
        
        Args:
            url (str): Target URL
        """
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")
    
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
        self.logger.info("Page refreshed")
    
    def scroll_to_element(self, locator):
        """Scroll to an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled to element: {locator}")
