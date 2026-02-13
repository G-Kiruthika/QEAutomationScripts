from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class SeleniumWrapper:
    """Wrapper class for common Selenium operations with enhanced error handling"""
    
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
    
    def wait_for_element(self, locator, timeout=None, condition='presence'):
        """
        Wait for element with specified condition
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout, uses default if None
            condition (str): Wait condition - 'presence', 'visible', 'clickable'
        
        Returns:
            WebElement: Found element
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        
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
            raise TimeoutException(f"Element {locator} not found within {wait_time} seconds with condition '{condition}'")
    
    def click_element(self, locator, timeout=None):
        """
        Click on element after waiting for it to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        """
        element = self.wait_for_element(locator, timeout, condition='clickable')
        element.click()
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """
        Enter text into element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            text (str): Text to enter
            timeout (int): Custom timeout
            clear_first (bool): Clear field before entering text
        """
        element = self.wait_for_element(locator, timeout, condition='visible')
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator, timeout=None):
        """
        Get text from element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element(locator, timeout, condition='visible')
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout, condition='visible')
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=5):
        """
        Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout, condition='presence')
            return True
        except TimeoutException:
            return False
    
    def get_element_attribute(self, locator, attribute, timeout=None):
        """
        Get attribute value from element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            attribute (str): Attribute name
            timeout (int): Custom timeout
        
        Returns:
            str: Attribute value
        """
        element = self.wait_for_element(locator, timeout, condition='presence')
        return element.get_attribute(attribute)
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """
        Wait for URL to contain specified fragment
        
        Args:
            url_fragment (str): URL fragment to wait for
            timeout (int): Custom timeout
        
        Returns:
            bool: True if URL contains fragment
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.url_contains(url_fragment))
    
    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        """
        element = self.wait_for_element(locator, timeout, condition='presence')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Brief pause after scroll
