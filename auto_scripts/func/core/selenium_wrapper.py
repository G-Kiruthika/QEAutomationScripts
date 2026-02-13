# core/selenium_wrapper.py
# Selenium wrapper with common utility methods for element interactions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time


class SeleniumWrapper:
    """
    Wrapper class for common Selenium operations with enhanced error handling
    """
    
    def __init__(self, driver, timeout=20):
        """
        Initialize SeleniumWrapper
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for explicit waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for element to be present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: Found element
        """
        wait_time = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found within {wait_time} seconds")
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: Visible element
        """
        wait_time = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible within {wait_time} seconds")
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: Clickable element
        """
        wait_time = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable within {wait_time} seconds")
    
    def click_element(self, locator, wait_for_clickable=True):
        """
        Click on element with optional wait
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            wait_for_clickable (bool): Wait for element to be clickable
        """
        if wait_for_clickable:
            element = self.wait_for_element_clickable(locator)
        else:
            element = self.wait_for_element(locator)
        element.click()
    
    def enter_text(self, locator, text, clear_first=True):
        """
        Enter text into input field
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            text (str): Text to enter
            clear_first (bool): Clear field before entering text
        """
        element = self.wait_for_element_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """
        Get text from element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Timeout for check
        
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
    
    def is_element_present(self, locator, timeout=5):
        """
        Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Timeout for check
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator):
        """
        Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
        """
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Small delay after scroll
    
    def hover_over_element(self, locator):
        """
        Hover over element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
        """
        element = self.wait_for_element_visible(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
    def get_attribute(self, locator, attribute_name):
        """
        Get attribute value from element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            attribute_name (str): Name of attribute
        
        Returns:
            str: Attribute value
        """
        element = self.wait_for_element(locator)
        return element.get_attribute(attribute_name)
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """
        Wait for URL to contain specific fragment
        
        Args:
            url_fragment (str): URL fragment to check
            timeout (int): Custom timeout (optional)
        
        Returns:
            bool: True if URL contains fragment
        """
        wait_time = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.url_contains(url_fragment)
            )
        except TimeoutException:
            raise TimeoutException(f"URL does not contain '{url_fragment}' within {wait_time} seconds")