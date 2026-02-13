# Selenium Wrapper with common utility methods
# Provides reusable methods for element interactions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import yaml
import os


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


class SeleniumWrapper:
    """Wrapper class for common Selenium operations"""
    
    def __init__(self, driver):
        self.driver = driver
        config = load_config()
        self.explicit_wait = config['ui'].get('explicit_wait', 20)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
            timeout (int): Wait timeout in seconds
        
        Returns:
            WebElement: Found element
        """
        if timeout is None:
            timeout = self.explicit_wait
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element not found: {locator}")
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
            timeout (int): Wait timeout in seconds
        
        Returns:
            WebElement: Visible element
        """
        if timeout is None:
            timeout = self.explicit_wait
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element not visible: {locator}")
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
            timeout (int): Wait timeout in seconds
        
        Returns:
            WebElement: Clickable element
        """
        if timeout is None:
            timeout = self.explicit_wait
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element not clickable: {locator}")
    
    def click_element(self, locator):
        """Click on element
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
        """
        element = self.wait_for_element_clickable(locator)
        element.click()
    
    def enter_text(self, locator, text):
        """Enter text into element
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
            text (str): Text to enter
        """
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from element
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.*, value)
            timeout (int): Wait timeout in seconds
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
