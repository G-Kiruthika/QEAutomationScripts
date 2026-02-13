from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Base Page Object Model class with common methods"""

    def __init__(self, driver, timeout=10):
        """Initialize BasePage with driver and default timeout"""
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find_element(self, locator):
        """Find element with explicit wait"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise NoSuchElementException(f"Element not found: {locator}")

    def find_elements(self, locator):
        """Find multiple elements"""
        return self.driver.find_elements(*locator)

    def click_element(self, locator):
        """Click on an element"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator, text):
        """Enter text into an input field"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator):
        """Get text from an element"""
        element = self.find_element(locator)
        return element.text

    def get_element_attribute(self, locator, attribute):
        """Get attribute value from an element"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator):
        """Check if element is present in DOM"""
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_element_to_disappear(self, locator):
        """Wait for element to disappear"""
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def switch_to_frame(self, locator):
        """Switch to iframe"""
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self):
        """Switch back to default content"""
        self.driver.switch_to.default_content()

    def get_page_title(self):
        """Get page title"""
        return self.driver.title

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
