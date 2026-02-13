"""Selenium Wrapper Module

This module provides wrapper methods for common Selenium operations.
Enhances reliability with explicit waits and error handling.
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class SeleniumWrapper:
    """Wrapper class for Selenium WebDriver operations"""

    def __init__(self, driver, timeout=10):
        """Initialize SeleniumWrapper
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for explicit waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, locator, timeout=None):
        """Find element with explicit wait
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            WebElement: Found element
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator, timeout=None):
        """Find multiple elements with explicit wait
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            list: List of found WebElements
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator, timeout=None):
        """Click element with explicit wait for clickability
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if click successful
        """
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return True
        except (TimeoutException, ElementNotInteractableException) as e:
            print(f"Error clicking element {locator}: {str(e)}")
            return False

    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """Enter text into input field
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to enter
            clear_first (bool): Whether to clear field before entering text
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if text entry successful
        """
        try:
            element = self.find_element(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            print(f"Error entering text into {locator}: {str(e)}")
            return False

    def get_text(self, locator, timeout=None):
        """Get text from element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            str: Element text or empty string if error
        """
        try:
            element = self.find_element(locator, timeout)
            return element.text
        except Exception as e:
            print(f"Error getting text from {locator}: {str(e)}")
            return ""

    def get_attribute(self, locator, attribute_name, timeout=None):
        """Get attribute value from element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            attribute_name (str): Name of attribute to retrieve
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            str: Attribute value or None if error
        """
        try:
            element = self.find_element(locator, timeout)
            return element.get_attribute(attribute_name)
        except Exception as e:
            print(f"Error getting attribute {attribute_name} from {locator}: {str(e)}")
            return None

    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=None):
        """Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, locator, timeout=None):
        """Check if element is clickable
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if element is clickable, False otherwise
        """
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear from DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if element disappeared, False if still present
        """
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if scroll successful
        """
        try:
            element = self.find_element(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Brief pause after scroll
            return True
        except Exception as e:
            print(f"Error scrolling to element {locator}: {str(e)}")
            return False

    def hover_over_element(self, locator, timeout=None):
        """Hover mouse over element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if hover successful
        """
        try:
            element = self.find_element(locator, timeout)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            return True
        except Exception as e:
            print(f"Error hovering over element {locator}: {str(e)}")
            return False

    def select_dropdown_by_text(self, locator, text, timeout=None):
        """Select dropdown option by visible text
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Visible text of option to select
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if selection successful
        """
        try:
            from selenium.webdriver.support.ui import Select
            element = self.find_element(locator, timeout)
            select = Select(element)
            select.select_by_visible_text(text)
            return True
        except Exception as e:
            print(f"Error selecting dropdown option {text} from {locator}: {str(e)}")
            return False

    def switch_to_frame(self, locator, timeout=None):
        """Switch to iframe
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int, optional): Custom timeout for this operation
            
        Returns:
            bool: True if switch successful
        """
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
            return True
        except TimeoutException:
            return False

    def switch_to_default_content(self):
        """Switch back to default content from iframe
        
        Returns:
            bool: True if switch successful
        """
        try:
            self.driver.switch_to.default_content()
            return True
        except Exception as e:
            print(f"Error switching to default content: {str(e)}")
            return False

    def take_screenshot(self, filepath):
        """Take screenshot and save to file
        
        Args:
            filepath (str): Path where screenshot should be saved
            
        Returns:
            bool: True if screenshot saved successfully
        """
        try:
            self.driver.save_screenshot(filepath)
            return True
        except Exception as e:
            print(f"Error taking screenshot: {str(e)}")
            return False

    def execute_javascript(self, script, *args):
        """Execute JavaScript code
        
        Args:
            script (str): JavaScript code to execute
            *args: Arguments to pass to the script
            
        Returns:
            Any: Result of JavaScript execution
        """
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            print(f"Error executing JavaScript: {str(e)}")
            return None
