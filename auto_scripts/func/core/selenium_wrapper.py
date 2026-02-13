# core/selenium_wrapper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import yaml
import os

class SeleniumWrapper:
    """
    Wrapper class for common Selenium operations with enhanced error handling
    """
    
    def __init__(self, driver):
        self.driver = driver
        
        # Load wait timeout from config
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path) as f:
            config = yaml.safe_load(f)
        self.explicit_wait = config['ui'].get('explicit_wait', 20)
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for element to be present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        
        Returns:
            WebElement: Found element
        """
        timeout = timeout or self.explicit_wait
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found within {timeout} seconds")
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        
        Returns:
            WebElement: Visible element
        """
        timeout = timeout or self.explicit_wait
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible within {timeout} seconds")
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        
        Returns:
            WebElement: Clickable element
        """
        timeout = timeout or self.explicit_wait
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable within {timeout} seconds")
    
    def click_element(self, locator, timeout=None):
        """
        Click on element after waiting for it to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """
        Enter text into element after waiting for it to be visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            text (str): Text to enter
            timeout (int): Wait timeout in seconds
            clear_first (bool): Clear field before entering text
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """
        Get text from element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=2):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_element_present(self, locator, timeout=2):
        """
        Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def hover_over_element(self, locator, timeout=None):
        """
        Hover over element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
        """
        element = self.wait_for_element_visible(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        """
        Get attribute value from element
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            attribute_name (str): Name of attribute
            timeout (int): Wait timeout in seconds
        
        Returns:
            str: Attribute value
        """
        element = self.wait_for_element(locator, timeout)
        return element.get_attribute(attribute_name)
    
    def switch_to_frame(self, frame_locator, timeout=None):
        """
        Switch to iframe
        
        Args:
            frame_locator (tuple): Frame locator tuple
            timeout (int): Wait timeout in seconds
        """
        frame = self.wait_for_element(frame_locator, timeout)
        self.driver.switch_to.frame(frame)
    
    def switch_to_default_content(self):
        """
        Switch back to default content from iframe
        """
        self.driver.switch_to.default_content()
