from core.selenium_wrapper import SeleniumWrapper
import yaml
import os


class BasePage:
    """Base class for all page objects with common functionality"""
    
    def __init__(self, driver):
        self.driver = driver
        self.selenium_wrapper = SeleniumWrapper(driver)
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from config.yaml"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def find_element(self, locator, timeout=None):
        """Find element using selenium wrapper"""
        return self.selenium_wrapper.find_element(locator, timeout)
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements using selenium wrapper"""
        return self.selenium_wrapper.find_elements(locator, timeout)
    
    def click_element(self, locator, timeout=None):
        """Click element using selenium wrapper"""
        self.selenium_wrapper.click_element(locator, timeout)
    
    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """Enter text into element using selenium wrapper"""
        self.selenium_wrapper.enter_text(locator, text, clear_first, timeout)
    
    def get_text(self, locator, timeout=None):
        """Get text from element using selenium wrapper"""
        return self.selenium_wrapper.get_text(locator, timeout)
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        """Get attribute value from element using selenium wrapper"""
        return self.selenium_wrapper.get_attribute(locator, attribute_name, timeout)
    
    def is_element_visible(self, locator, timeout=2):
        """Check if element is visible using selenium wrapper"""
        return self.selenium_wrapper.is_element_visible(locator, timeout)
    
    def is_element_present(self, locator, timeout=2):
        """Check if element is present using selenium wrapper"""
        return self.selenium_wrapper.is_element_present(locator, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible using selenium wrapper"""
        return self.selenium_wrapper.wait_for_element_visible(locator, timeout)
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable using selenium wrapper"""
        return self.selenium_wrapper.wait_for_element_clickable(locator, timeout)
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element using selenium wrapper"""
        self.selenium_wrapper.scroll_to_element(locator, timeout)
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element using selenium wrapper"""
        self.selenium_wrapper.hover_over_element(locator, timeout)
    
    def take_screenshot(self, filename):
        """Take screenshot using selenium wrapper"""
        self.selenium_wrapper.take_screenshot(filename)
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
    
    def navigate_back(self):
        """Navigate back in browser history"""
        self.driver.back()
    
    def navigate_forward(self):
        """Navigate forward in browser history"""
        self.driver.forward()
    
    def switch_to_window(self, window_handle):
        """Switch to specific browser window"""
        self.driver.switch_to.window(window_handle)
    
    def get_window_handles(self):
        """Get all browser window handles"""
        return self.driver.window_handles
    
    def close_current_window(self):
        """Close current browser window"""
        self.driver.close()
    
    def switch_to_frame(self, frame_locator):
        """Switch to iframe"""
        frame_element = self.find_element(frame_locator)
        self.driver.switch_to.frame(frame_element)
    
    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()
    
    def execute_javascript(self, script, *args):
        """Execute JavaScript code"""
        return self.driver.execute_script(script, *args)
    
    def get_page_source(self):
        """Get page source HTML"""
        return self.driver.page_source