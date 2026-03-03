from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    StaleElementReferenceException
)
import time
import os
from datetime import datetime


class SeleniumWrapper:
    """Enhanced Selenium WebDriver wrapper with additional functionality"""
    
    def __init__(self, driver, default_timeout=10):
        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(driver, default_timeout)
        self.actions = ActionChains(driver)
    
    def wait_for_element_present(self, locator, timeout=None):
        """Wait for element to be present in DOM
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout, uses default if None
            
        Returns:
            WebElement: Found element
        """
        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout, uses default if None
            
        Returns:
            WebElement: Visible element
        """
        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout, uses default if None
            
        Returns:
            WebElement: Clickable element
        """
        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def safe_click(self, locator, timeout=None, retries=3):
        """Safely click element with retry mechanism
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
            retries (int): Number of retry attempts
        """
        for attempt in range(retries):
            try:
                element = self.wait_for_element_clickable(locator, timeout)
                element.click()
                return
            except (StaleElementReferenceException, ElementNotInteractableException):
                if attempt == retries - 1:
                    raise
                time.sleep(0.5)
    
    def safe_send_keys(self, locator, text, timeout=None, clear_first=True):
        """Safely send keys to element
        
        Args:
            locator (tuple): Element locator
            text (str): Text to send
            timeout (int): Custom timeout
            clear_first (bool): Clear field before entering text
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator, timeout=None):
        """Get text from element
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
            
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def get_element_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from element
        
        Args:
            locator (tuple): Element locator
            attribute (str): Attribute name
            timeout (int): Custom timeout
            
        Returns:
            str: Attribute value
        """
        element = self.wait_for_element_present(locator, timeout)
        return element.get_attribute(attribute)
    
    def is_element_displayed(self, locator, timeout=5):
        """Check if element is displayed
        
        Args:
            locator (tuple): Element locator
            timeout (int): Timeout for check
            
        Returns:
            bool: True if displayed, False otherwise
        """
        try:
            element = self.wait_for_element_present(locator, timeout)
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def is_element_enabled(self, locator, timeout=None):
        """Check if element is enabled
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
            
        Returns:
            bool: True if enabled, False otherwise
        """
        element = self.wait_for_element_present(locator, timeout)
        return element.is_enabled()
    
    def select_dropdown_by_text(self, locator, text, timeout=None):
        """Select dropdown option by visible text
        
        Args:
            locator (tuple): Dropdown element locator
            text (str): Visible text to select
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_present(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def select_dropdown_by_value(self, locator, value, timeout=None):
        """Select dropdown option by value
        
        Args:
            locator (tuple): Dropdown element locator
            value (str): Value to select
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_present(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_visible(locator, timeout)
        self.actions.move_to_element(element).perform()
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_present(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def take_screenshot(self, filename=None):
        """Take screenshot
        
        Args:
            filename (str): Custom filename, auto-generated if None
            
        Returns:
            str: Screenshot file path
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Ensure screenshots directory exists
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath
    
    def switch_to_frame(self, locator_or_index, timeout=None):
        """Switch to iframe
        
        Args:
            locator_or_index: Frame locator tuple or index
            timeout (int): Custom timeout
        """
        if isinstance(locator_or_index, tuple):
            frame_element = self.wait_for_element_present(locator_or_index, timeout)
            self.driver.switch_to.frame(frame_element)
        else:
            self.driver.switch_to.frame(locator_or_index)
    
    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_handle):
        """Switch to specific window
        
        Args:
            window_handle (str): Window handle to switch to
        """
        self.driver.switch_to.window(window_handle)
    
    def get_all_window_handles(self):
        """Get all window handles
        
        Returns:
            list: List of window handles
        """
        return self.driver.window_handles
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to load completely
        
        Args:
            timeout (int): Maximum wait time
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def execute_javascript(self, script, *args):
        """Execute JavaScript code
        
        Args:
            script (str): JavaScript code to execute
            *args: Arguments to pass to the script
            
        Returns:
            Any: Script execution result
        """
        return self.driver.execute_script(script, *args)