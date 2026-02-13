# core/wait_helper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WaitHelper:
    """Enhanced wait helper for common wait scenarios in registration flow"""
    
    def __init__(self, driver, timeout=10):
        """Initialize WaitHelper
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_visible(self, locator):
        """Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
        
        Returns:
            WebElement: The visible element
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible after {self.timeout} seconds")
    
    def wait_for_element_clickable(self, locator):
        """Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
        
        Returns:
            WebElement: The clickable element
        """
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable after {self.timeout} seconds")
    
    def wait_for_element_present(self, locator):
        """Wait for element to be present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
        
        Returns:
            WebElement: The present element
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not present after {self.timeout} seconds")
    
    def wait_for_text_in_element(self, locator, text):
        """Wait for specific text to appear in element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            text (str): Expected text
        
        Returns:
            bool: True if text appears in element
        """
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            raise TimeoutException(f"Text '{text}' not found in element {locator} after {self.timeout} seconds")
    
    def wait_for_url_contains(self, url_fragment):
        """Wait for URL to contain specific fragment
        
        Args:
            url_fragment (str): URL fragment to wait for
        
        Returns:
            bool: True if URL contains fragment
        """
        try:
            return self.wait.until(EC.url_contains(url_fragment))
        except TimeoutException:
            raise TimeoutException(f"URL does not contain '{url_fragment}' after {self.timeout} seconds")
    
    def wait_for_alert_present(self):
        """Wait for alert to be present
        
        Returns:
            Alert: The alert object
        """
        try:
            return self.wait.until(EC.alert_is_present())
        except TimeoutException:
            raise TimeoutException(f"Alert not present after {self.timeout} seconds")