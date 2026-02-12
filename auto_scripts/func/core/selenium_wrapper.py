# core/selenium_wrapper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumWrapper:
 """
 Wrapper class providing enhanced Selenium WebDriver methods with explicit waits.
 """
 
 def __init__(self, driver, timeout=10):
 """
 Initialize the SeleniumWrapper.
 
 Args:
 driver: WebDriver instance
 timeout (int): Default timeout for waits in seconds
 """
 self.driver = driver
 self.timeout = timeout
 self.wait = WebDriverWait(driver, timeout)
 
 def wait_for_element(self, locator, timeout=None):
 """
 Wait for an element to be present in the DOM.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 
 Returns:
 WebElement: The found element
 """
 wait_time = timeout if timeout else self.timeout
 wait = WebDriverWait(self.driver, wait_time)
 return wait.until(EC.presence_of_element_located(locator))
 
 def wait_for_element_visible(self, locator, timeout=None):
 """
 Wait for an element to be visible.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 
 Returns:
 WebElement: The visible element
 """
 wait_time = timeout if timeout else self.timeout
 wait = WebDriverWait(self.driver, wait_time)
 return wait.until(EC.visibility_of_element_located(locator))
 
 def wait_for_element_clickable(self, locator, timeout=None):
 """
 Wait for an element to be clickable.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 
 Returns:
 WebElement: The clickable element
 """
 wait_time = timeout if timeout else self.timeout
 wait = WebDriverWait(self.driver, wait_time)
 return wait.until(EC.element_to_be_clickable(locator))
 
 def click_element(self, locator, timeout=None):
 """
 Wait for element to be clickable and click it.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 """
 element = self.wait_for_element_clickable(locator, timeout)
 element.click()
 
 def enter_text(self, locator, text, timeout=None, clear_first=True):
 """
 Wait for element and enter text.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 text (str): Text to enter
 timeout (int): Custom timeout, uses default if None
 clear_first (bool): Clear field before entering text
 """
 element = self.wait_for_element_visible(locator, timeout)
 if clear_first:
 element.clear()
 element.send_keys(text)
 
 def get_text(self, locator, timeout=None):
 """
 Wait for element and get its text.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 
 Returns:
 str: Element text
 """
 element = self.wait_for_element_visible(locator, timeout)
 return element.text
 
 def is_element_visible(self, locator, timeout=2):
 """
 Check if element is visible within timeout.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Timeout in seconds
 
 Returns:
 bool: True if visible, False otherwise
 """
 try:
 wait = WebDriverWait(self.driver, timeout)
 wait.until(EC.visibility_of_element_located(locator))
 return True
 except TimeoutException:
 return False
 
 def is_element_present(self, locator, timeout=2):
 """
 Check if element is present in DOM within timeout.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Timeout in seconds
 
 Returns:
 bool: True if present, False otherwise
 """
 try:
 wait = WebDriverWait(self.driver, timeout)
 wait.until(EC.presence_of_element_located(locator))
 return True
 except TimeoutException:
 return False
 
 def scroll_to_element(self, locator, timeout=None):
 """
 Scroll to element.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 """
 element = self.wait_for_element(locator, timeout)
 self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
 
 def hover_over_element(self, locator, timeout=None):
 """
 Hover over element.
 
 Args:
 locator (tuple): Locator tuple (By.ID, 'element_id')
 timeout (int): Custom timeout, uses default if None
 """
 element = self.wait_for_element_visible(locator, timeout)
 actions = ActionChains(self.driver)
 actions.move_to_element(element).perform()
