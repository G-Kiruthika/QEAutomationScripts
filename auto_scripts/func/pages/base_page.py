# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from core.selenium_wrapper import SeleniumWrapper


class BasePage:
 """
 Base Page class that all page objects inherit from.
 Provides common functionality for all pages.
 """
 
 def __init__(self, driver, timeout=10):
 """
 Initialize BasePage.
 
 Args:
 driver: WebDriver instance
 timeout (int): Default timeout for waits
 """
 self.driver = driver
 self.timeout = timeout
 self.wrapper = SeleniumWrapper(driver, timeout)
 
 def open(self, url=None):
 """
 Navigate to a URL.
 
 Args:
 url (str): URL to navigate to. If None, uses self.url
 """
 target_url = url if url else getattr(self, 'url', None)
 if target_url:
 self.driver.get(target_url)
 else:
 raise ValueError("No URL provided and page class has no default URL")
 
 def find_element(self, locator, timeout=None):
 """
 Find an element with explicit wait.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 
 Returns:
 WebElement: The found element
 """
 return self.wrapper.wait_for_element(locator, timeout)
 
 def find_elements(self, locator, timeout=None):
 """
 Find multiple elements with explicit wait.
 
 Args:
 locator (tuple): Locator tuple (By.CLASS_NAME, 'class_name')
 timeout (int): Custom timeout, uses default if None
 
 Returns:
 list: List of WebElements
 """
 wait_time = timeout if timeout else self.timeout
 wait = WebDriverWait(self.driver, wait_time)
 return wait.until(EC.presence_of_all_elements_located(locator))
 
 def click_element(self, locator, timeout=None):
 """
 Click an element with explicit wait.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 """
 self.wrapper.click_element(locator, timeout)
 
 def enter_text(self, locator, text, timeout=None, clear_first=True):
 """
 Enter text into an element.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 text (str): Text to enter
 timeout (int): Custom timeout, uses default if None
 clear_first (bool): Clear field before entering text
 """
 self.wrapper.enter_text(locator, text, timeout, clear_first)
 
 def get_text(self, locator, timeout=None):
 """
 Get text from an element.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 
 Returns:
 str: Element text
 """
 return self.wrapper.get_text(locator, timeout)
 
 def is_element_visible(self, locator, timeout=2):
 """
 Check if element is visible.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Timeout in seconds
 
 Returns:
 bool: True if visible, False otherwise
 """
 return self.wrapper.is_element_visible(locator, timeout)
 
 def is_element_present(self, locator, timeout=2):
 """
 Check if element is present in DOM.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Timeout in seconds
 
 Returns:
 bool: True if present, False otherwise
 """
 return self.wrapper.is_element_present(locator, timeout)
 
 def get_current_url(self):
 """
 Get current page URL.
 
 Returns:
 str: Current URL
 """
 return self.driver.current_url
 
 def get_page_title(self):
 """
 Get page title.
 
 Returns:
 str: Page title
 """
 return self.driver.title
 
 def scroll_to_element(self, locator, timeout=None):
 """
 Scroll to element.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 """
 self.wrapper.scroll_to_element(locator, timeout)
 
 def refresh_page(self):
 """
 Refresh the current page.
 """
 self.driver.refresh()
