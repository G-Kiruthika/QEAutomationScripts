# core/selenium_wrapper.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(driver, locator, timeout=10):
 return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def click_element(driver, locator):
 element = wait_for_element(driver, locator)
 element.click()

def enter_text(driver, locator, text):
 element = wait_for_element(driver, locator)
 element.clear()
 element.send_keys(text)
