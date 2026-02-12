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
import time


class SeleniumWrapper:
 """
 Wrapper class providing enhanced Selenium WebDriver operations with robust error handling.
 """
 
 def __init__(self, driver, timeout=10):
 """
 Initialize SeleniumWrapper.
 
 Args:
 driver: WebDriver instance
 timeout (int): Default timeout for wait operations
 """
 self.driver = driver
 self.timeout = timeout
 self.wait = WebDriverWait(driver, timeout)
 
 def wait_for_element(self, locator, timeout=None, condition='presence'):
 """
 Wait for an element with specified condition.
 
 Args:
 locator (tuple): Element locator (By.ID, 'element_id')
 timeout (int, optional): Custom timeout. Defaults to instance timeout.
 condition (str): Wait condition - 'presence', 'visible', 'clickable'
 
 Returns:
 WebElement: Located element
 """
 wait_timeout = timeout or self.timeout
 wait = WebDriverWait(self.driver, wait_timeout)
 
 try:
 if condition == 'presence':
 return wait.until(EC.presence_of_element_located(locator))
 elif condition == 'visible':
 return wait.until(EC.visibility_of_element_located(locator))
 elif condition == 'clickable':
 return wait.until(EC.element_to_be_clickable(locator))
 else:
 raise ValueError(f"Invalid condition: {condition}")
 except TimeoutException:
 raise TimeoutException(f"Element {locator} not found within {wait_timeout} seconds with condition '{condition}'")
 
 def click_element(self, locator, timeout=None):
 """
 Click an element with wait and error handling.
 
 Args:
 locator (tuple): Element locator
 timeout (int, optional): Custom timeout
 """
 try:
 element = self.wait_for_element(locator, timeout, condition='clickable')
 element.click()
 except (ElementNotInteractableException, StaleElementReferenceException):
 # Retry with JavaScript click if normal click fails
 element = self.wait_for_element(locator, timeout, condition='presence')
 self.driver.execute_script("arguments[0].click();", element)
 
 def enter_text(self, locator, text, timeout=None, clear_first=True):
 """
 Enter text into an input field.
 
 Args:
 locator (tuple): Element locator
 text (str): Text to enter
 timeout (int, optional): Custom timeout
 clear_first (bool): Clear field before entering text
 """
 element = self.wait_for_element(locator, timeout, condition='visible')
 if clear_first:
 element.clear()
 element.send_keys(text)
 
 def get_element_text(self, locator, timeout=None):
 """
 Get text from an element.
 
 Args:
 locator (tuple): Element locator
 timeout (int, optional): Custom timeout
 
 Returns:
 str: Element text
 """
 element = self.wait_for_element(locator, timeout, condition='visible')
 return element.text
 
 def is_element_visible(self, locator, timeout=None):
 """
 Check if element is visible.
 
 Args:
 locator (tuple): Element locator
 timeout (int, optional): Custom timeout
 
 Returns:
 bool: True if visible, False otherwise
 """
 try:
 self.wait_for_element(locator, timeout or 5, condition='visible')
 return True
 except TimeoutException:
 return False
 
 def is_element_present(self, locator, timeout=None):
 """
 Check if element is present in DOM.
 
 Args:
 locator (tuple): Element locator
 timeout (int, optional): Custom timeout
 
 Returns:
 bool: True if present, False otherwise
 """
 try:
 self.wait_for_element(locator, timeout or 5, condition='presence')
 return True
 except TimeoutException:
 return False
 
 def get_element_attribute(self, locator, attribute, timeout=None):
 """
 Get attribute value from an element.
 
 Args:
 locator (tuple): Element locator
 attribute (str): Attribute name
 timeout (int, optional): Custom timeout
 
 Returns:
 str: Attribute value
 """
 element = self.wait_for_element(locator, timeout, condition='presence')
 return element.get_attribute(attribute)
 
 def select_dropdown_by_text(self, locator, text, timeout=None):
 """
 Select dropdown option by visible text.
 
 Args:
 locator (tuple): Dropdown locator
 text (str): Visible text to select
 timeout (int, optional): Custom timeout
 """
 from selenium.webdriver.support.select import Select
 element = self.wait_for_element(locator, timeout, condition='visible')
 select = Select(element)
 select.select_by_visible_text(text)
 
 def hover_over_element(self, locator, timeout=None):
 """
 Hover mouse over an element.
 
 Args:
 locator (tuple): Element locator
 timeout (int, optional): Custom timeout
 """
 element = self.wait_for_element(locator, timeout, condition='visible')
 actions = ActionChains(self.driver)
 actions.move_to_element(element).perform()
 
 def scroll_to_element(self, locator, timeout=None):
 """
 Scroll to bring element into view.
 
 Args:
 locator (tuple): Element locator
 timeout (int, optional): Custom timeout
 """
 element = self.wait_for_element(locator, timeout, condition='presence')
 self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
 time.sleep(0.5) # Brief pause for scroll completion
 
 def switch_to_frame(self, locator_or_index, timeout=None):
 """
 Switch to iframe.
 
 Args:
 locator_or_index: Frame locator tuple or index
 timeout (int, optional): Custom timeout
 """
 if isinstance(locator_or_index, tuple):
 frame = self.wait_for_element(locator_or_index, timeout, condition='presence')
 self.driver.switch_to.frame(frame)
 else:
 self.driver.switch_to.frame(locator_or_index)
 
 def switch_to_default_content(self):
 """
 Switch back to default content from iframe.
 """
 self.driver.switch_to.default_content()
 
 def accept_alert(self, timeout=None):
 """
 Accept browser alert.
 
 Args:
 timeout (int, optional): Custom timeout
 """
 wait_timeout = timeout or self.timeout
 wait = WebDriverWait(self.driver, wait_timeout)
 alert = wait.until(EC.alert_is_present())
 alert.accept()
 
 def dismiss_alert(self, timeout=None):
 """
 Dismiss browser alert.
 
 Args:
 timeout (int, optional): Custom timeout
 """
 wait_timeout = timeout or self.timeout
 wait = WebDriverWait(self.driver, wait_timeout)
 alert = wait.until(EC.alert_is_present())
 alert.dismiss()
 
 def get_alert_text(self, timeout=None):
 """
 Get text from browser alert.
 
 Args:
 timeout (int, optional): Custom timeout
 
 Returns:
 str: Alert text
 """
 wait_timeout = timeout or self.timeout
 wait = WebDriverWait(self.driver, wait_timeout)
 alert = wait.until(EC.alert_is_present())
 return alert.text