from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import yaml
import os

class SeleniumWrapper:
    """Wrapper class for common Selenium operations"""
    
    def __init__(self, driver):
        self.driver = driver
        
        # Load configuration for timeout
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        self.timeout = config.get('environment', {}).get('timeout', 10)
        self.wait = WebDriverWait(self.driver, self.timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for element to be present and visible
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        Returns: WebElement
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def click_element(self, locator, timeout=None):
        """
        Click on element after waiting for it to be clickable
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text, timeout=None):
        """
        Enter text into element after waiting for it to be visible
        Args:
            locator: Tuple of (By, value)
            text: Text to enter
            timeout: Optional timeout override
        """
        element = self.wait_for_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator, timeout=None):
        """
        Get text from element
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        Returns: Element text
        """
        element = self.wait_for_element(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=None):
        """
        Check if element is visible
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        Returns: Boolean
        """
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def find_element(self, locator):
        """
        Find element by locator
        Args:
            locator: Tuple of (By, value)
        Returns: WebElement
        """
        return self.driver.find_element(*locator)