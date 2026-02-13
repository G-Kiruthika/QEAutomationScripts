# core/selenium_wrapper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging


class SeleniumWrapper:
    """
    Wrapper class providing enhanced Selenium WebDriver operations.
    """
    
    def __init__(self, driver, timeout=20):
        """
        Initialize the SeleniumWrapper.
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for explicit waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for an element to be present in the DOM.
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: The located element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            logging.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logging.error(f"Element not found within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for an element to be visible.
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: The visible element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logging.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logging.error(f"Element not visible within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for an element to be clickable.
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        
        Returns:
            WebElement: The clickable element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            logging.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logging.error(f"Element not clickable within {wait_time} seconds: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """
        Click an element after waiting for it to be clickable.
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
        logging.info(f"Clicked element: {locator}")
    
    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """
        Enter text into an input field.
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            text (str): Text to enter
            clear_first (bool): Clear field before entering text
            timeout (int): Custom timeout (optional)
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logging.info(f"Entered text '{text}' into element: {locator}")
    
    def get_text(self, locator, timeout=None):
        """
        Get text from an element.
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout (optional)
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator, timeout)
        text = element.text
        logging.debug(f"Retrieved text '{text}' from element: {locator}")
        return text
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if an element is visible.
        
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
        Check if an element is present in the DOM.
        
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