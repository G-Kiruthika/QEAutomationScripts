from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)


class ValidationHelpers:
    """Reusable validation helper methods for test automation"""
    
    def __init__(self, driver, timeout=10):
        """Initialize validation helpers
        
        Args:
            driver: WebDriver instance
            timeout: Default timeout for waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Optional timeout override
        
        Returns:
            WebElement: The visible element
        
        Raises:
            TimeoutException: If element not visible within timeout
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Optional timeout override
        
        Returns:
            WebElement: The clickable element
        
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            logger.info(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_text_present(self, locator, expected_text, timeout=None):
        """Wait for specific text to be present in element
        
        Args:
            locator: Tuple of (By, locator_value)
            expected_text: Text to wait for
            timeout: Optional timeout override
        
        Returns:
            bool: True if text present
        
        Raises:
            TimeoutException: If text not present within timeout
        """
        wait_time = timeout or self.timeout
        try:
            result = WebDriverWait(self.driver, wait_time).until(
                EC.text_to_be_present_in_element(locator, expected_text)
            )
            logger.info(f"Text '{expected_text}' present in element: {locator}")
            return result
        except TimeoutException:
            logger.error(f"Text '{expected_text}' not present within {wait_time} seconds: {locator}")
            raise
    
    def is_element_present(self, locator):
        """Check if element is present in DOM
        
        Args:
            locator: Tuple of (By, locator_value)
        
        Returns:
            bool: True if element present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            logger.info(f"Element present: {locator}")
            return True
        except NoSuchElementException:
            logger.info(f"Element not present: {locator}")
            return False
    
    def is_element_visible(self, locator):
        """Check if element is visible
        
        Args:
            locator: Tuple of (By, locator_value)
        
        Returns:
            bool: True if element visible, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            is_visible = element.is_displayed()
            logger.info(f"Element visibility: {locator} - {is_visible}")
            return is_visible
        except NoSuchElementException:
            logger.info(f"Element not found: {locator}")
            return False
    
    def is_element_enabled(self, locator):
        """Check if element is enabled
        
        Args:
            locator: Tuple of (By, locator_value)
        
        Returns:
            bool: True if element enabled, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            is_enabled = element.is_enabled()
            logger.info(f"Element enabled: {locator} - {is_enabled}")
            return is_enabled
        except NoSuchElementException:
            logger.info(f"Element not found: {locator}")
            return False
    
    def get_element_text(self, locator):
        """Get text from element
        
        Args:
            locator: Tuple of (By, locator_value)
        
        Returns:
            str: Element text
        """
        try:
            element = self.driver.find_element(*locator)
            text = element.text
            logger.info(f"Element text retrieved: {locator} - '{text}'")
            return text
        except NoSuchElementException:
            logger.error(f"Element not found: {locator}")
            return ""
    
    def get_element_attribute(self, locator, attribute_name):
        """Get attribute value from element
        
        Args:
            locator: Tuple of (By, locator_value)
            attribute_name: Name of the attribute
        
        Returns:
            str: Attribute value
        """
        try:
            element = self.driver.find_element(*locator)
            value = element.get_attribute(attribute_name)
            logger.info(f"Element attribute retrieved: {locator} - {attribute_name}='{value}'")
            return value
        except NoSuchElementException:
            logger.error(f"Element not found: {locator}")
            return None
    
    def verify_url_contains(self, expected_url_part):
        """Verify current URL contains expected part
        
        Args:
            expected_url_part: Expected URL substring
        
        Returns:
            bool: True if URL contains expected part
        """
        current_url = self.driver.current_url
        result = expected_url_part in current_url
        logger.info(f"URL verification: Expected '{expected_url_part}' in '{current_url}' - {result}")
        return result
    
    def verify_page_title(self, expected_title):
        """Verify page title matches expected
        
        Args:
            expected_title: Expected page title
        
        Returns:
            bool: True if title matches
        """
        actual_title = self.driver.title
        result = actual_title == expected_title
        logger.info(f"Title verification: Expected '{expected_title}', Actual '{actual_title}' - {result}")
        return result