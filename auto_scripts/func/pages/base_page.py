from core.selenium_wrapper import SeleniumWrapper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import yaml
import os


class BasePage:
    """Base page class that provides common functionality for all page objects."""
    
    def __init__(self, driver):
        self.driver = driver
        self.selenium_wrapper = SeleniumWrapper(driver)
        self.config = self._load_config()
        self.default_timeout = self.config.get('browser', {}).get('explicit_wait', 30)
    
    def _load_config(self):
        """Load configuration from config.yaml."""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return {'browser': {'explicit_wait': 30}}
    
    def open(self, url=None):
        """Open the page URL."""
        if url:
            self.driver.get(url)
        elif hasattr(self, 'PAGE_URL'):
            base_url = self.config.get('environment', {}).get('base_url', '')
            full_url = f"{base_url.rstrip('/')}/{self.PAGE_URL.lstrip('/')}"
            self.driver.get(full_url)
        else:
            raise ValueError("No URL provided and PAGE_URL not defined in page class")
    
    def get_page_title(self):
        """Get the current page title."""
        return self.driver.title
    
    def get_current_url(self):
        """Get the current page URL."""
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
    
    # Element interaction methods using selenium_wrapper
    def find_element(self, locator, timeout=None):
        """Find element using selenium wrapper."""
        return self.selenium_wrapper.find_element(locator, timeout)
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements using selenium wrapper."""
        return self.selenium_wrapper.find_elements(locator, timeout)
    
    def click_element(self, locator, timeout=None):
        """Click element using selenium wrapper."""
        self.selenium_wrapper.click_element(locator, timeout)
    
    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """Enter text into element using selenium wrapper."""
        self.selenium_wrapper.enter_text(locator, text, clear_first, timeout)
    
    def get_element_text(self, locator, timeout=None):
        """Get text from element using selenium wrapper."""
        return self.selenium_wrapper.get_element_text(locator, timeout)
    
    def get_element_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from element using selenium wrapper."""
        return self.selenium_wrapper.get_element_attribute(locator, attribute, timeout)
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present using selenium wrapper."""
        return self.selenium_wrapper.is_element_present(locator, timeout)
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible using selenium wrapper."""
        return self.selenium_wrapper.is_element_visible(locator, timeout)
    
    def is_element_clickable(self, locator, timeout=5):
        """Check if element is clickable using selenium wrapper."""
        return self.selenium_wrapper.is_element_clickable(locator, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present using selenium wrapper."""
        return self.selenium_wrapper.wait_for_element(locator, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible using selenium wrapper."""
        return self.selenium_wrapper.wait_for_element_visible(locator, timeout)
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable using selenium wrapper."""
        return self.selenium_wrapper.wait_for_element_clickable(locator, timeout)
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element using selenium wrapper."""
        self.selenium_wrapper.scroll_to_element(locator, timeout)
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element using selenium wrapper."""
        self.selenium_wrapper.hover_over_element(locator, timeout)
    
    def select_dropdown_by_text(self, locator, text, timeout=None):
        """Select dropdown option by text using selenium wrapper."""
        self.selenium_wrapper.select_dropdown_by_text(locator, text, timeout)
    
    def select_dropdown_by_value(self, locator, value, timeout=None):
        """Select dropdown option by value using selenium wrapper."""
        self.selenium_wrapper.select_dropdown_by_value(locator, value, timeout)
    
    def take_screenshot(self, filename=None):
        """Take screenshot using selenium wrapper."""
        return self.selenium_wrapper.take_screenshot(filename)
    
    def execute_javascript(self, script, *args):
        """Execute JavaScript using selenium wrapper."""
        return self.selenium_wrapper.execute_javascript(script, *args)
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load completely using selenium wrapper."""
        self.selenium_wrapper.wait_for_page_load(timeout)
    
    # Common validation methods
    def is_page_loaded(self):
        """Check if page is loaded. Override in child classes."""
        return True
    
    def wait_for_page_to_load(self, timeout=None):
        """Wait for page to load. Can be overridden in child classes."""
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self.is_page_loaded()
            )
        except TimeoutException:
            raise TimeoutException(f"Page did not load within {timeout} seconds")
    
    def get_page_source(self):
        """Get page source."""
        return self.driver.page_source
    
    def switch_to_frame(self, locator_or_index, timeout=None):
        """Switch to iframe."""
        self.selenium_wrapper.switch_to_frame(locator_or_index, timeout)
    
    def switch_to_default_content(self):
        """Switch back to default content."""
        self.selenium_wrapper.switch_to_default_content()
    
    def close_current_window(self):
        """Close current browser window."""
        self.driver.close()
    
    def quit_driver(self):
        """Quit the driver."""
        self.driver.quit()