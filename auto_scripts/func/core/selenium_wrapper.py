from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import yaml
import os


class SeleniumWrapper:
    """Wrapper class for common Selenium operations with enhanced error handling"""
    
    def __init__(self, driver, timeout=None):
        """Initialize SeleniumWrapper
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for explicit waits. If None, reads from config.
        """
        self.driver = driver
        
        if timeout is None:
            config = self._load_config()
            self.timeout = config.get('ui', {}).get('explicit_wait', 20)
        else:
            self.timeout = timeout
    
    def _load_config(self):
        """Load configuration from config.yaml"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout. If None, uses default.
        
        Returns:
            WebElement: The located element
        """
        wait_time = timeout if timeout else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found within {wait_time} seconds")
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout. If None, uses default.
        
        Returns:
            WebElement: The visible element
        """
        wait_time = timeout if timeout else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible within {wait_time} seconds")
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout. If None, uses default.
        
        Returns:
            WebElement: The clickable element
        """
        wait_time = timeout if timeout else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable within {wait_time} seconds")
    
    def click_element(self, locator, timeout=None):
        """Click on an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout. If None, uses default.
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """Enter text into an input field
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            text (str): Text to enter
            timeout (int): Custom timeout. If None, uses default.
            clear_first (bool): Clear field before entering text
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """Get text from an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout. If None, uses default.
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=2):
        """Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Timeout for check
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_element_present(self, locator, timeout=2):
        """Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Timeout for check
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from an element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            attribute (str): Attribute name
            timeout (int): Custom timeout. If None, uses default.
        
        Returns:
            str: Attribute value
        """
        element = self.wait_for_element(locator, timeout)
        return element.get_attribute(attribute)
    
    def switch_to_frame(self, locator, timeout=None):
        """Switch to iframe
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout. If None, uses default.
        """
        wait_time = timeout if timeout else self.timeout
        WebDriverWait(self.driver, wait_time).until(
            EC.frame_to_be_available_and_switch_to_it(locator)
        )
    
    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()
    
    def execute_script(self, script, *args):
        """Execute JavaScript
        
        Args:
            script (str): JavaScript code to execute
            *args: Arguments to pass to the script
        
        Returns:
            Any: Script execution result
        """
        return self.driver.execute_script(script, *args)
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout. If None, uses default.
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def take_screenshot(self, filepath):
        """Take screenshot and save to file
        
        Args:
            filepath (str): Path where screenshot should be saved
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.driver.save_screenshot(filepath)
            return True
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return False
