from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)

class SeleniumWrapper:
    """
    Wrapper class providing enhanced Selenium operations with explicit waits
    """
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for element to be present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout in seconds
        
        Returns:
            WebElement: Located element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found with locator: {locator}")
            raise
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout in seconds
        
        Returns:
            WebElement: Located element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not visible with locator: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Custom timeout in seconds
        
        Returns:
            WebElement: Located element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not clickable with locator: {locator}")
            raise
    
    def click_element(self, locator):
        """
        Click on element after waiting for it to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
        """
        element = self.wait_for_element_clickable(locator)
        element.click()
        logger.info(f"Clicked element: {locator}")
    
    def enter_text(self, locator, text):
        """
        Enter text into element after waiting for it to be visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            text (str): Text to enter
        """
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Entered text '{text}' into element: {locator}")
    
    def get_text(self, locator):
        """
        Get text from element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator)
        text = element.text
        logger.info(f"Retrieved text '{text}' from element: {locator}")
        return text
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Timeout in seconds
        
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
