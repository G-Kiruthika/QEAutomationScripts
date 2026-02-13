"""Base Page Module

Provides BasePage class with common UI actions and navigation.
All page objects should inherit from this class.
"""

from core.selenium_wrapper import SeleniumWrapper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


logger = logging.getLogger(__name__)


class BasePage:
    """Base Page class for all page objects
    
    Provides common methods for page interactions.
    """
    
    def __init__(self, driver):
        """
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wrapper = SeleniumWrapper(driver)
    
    def find_element(self, locator):
        """Find an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            WebElement: The found element
        """
        return self.wrapper.wait_for_element(locator)
    
    def click_element(self, locator):
        """Click an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        self.wrapper.click_element(locator)
    
    def enter_text(self, locator, text):
        """Enter text into an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to enter
        """
        self.wrapper.enter_text(locator, text)
    
    def get_text(self, locator):
        """Get text from an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            str: Element text
        """
        return self.wrapper.get_text(locator)
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            bool: True if visible, False otherwise
        """
        return self.wrapper.is_element_visible(locator, timeout)
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            bool: True if present, False otherwise
        """
        return self.wrapper.is_element_present(locator, timeout)
    
    def navigate_to(self, url):
        """Navigate to a URL
        
        Args:
            url (str): URL to navigate to
        """
        self.driver.get(url)
        logger.info(f"Navigated to: {url}")
    
    def get_current_url(self):
        """Get current URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def get_title(self):
        """Get page title
        
        Returns:
            str: Page title
        """
        return self.driver.title
