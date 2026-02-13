"""Base Test Class

Provides common setup and teardown functionality for all test classes.
Follows the Python UI Automation Framework standards.
"""

import pytest
import logging
from core.driver_factory import get_driver


logger = logging.getLogger(__name__)


class BaseTest:
    """Base class for all test classes.
    
    Provides common setup and teardown methods, driver management,
    and utility methods for test execution.
    """
    
    driver = None
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown fixture for tests.
        
        Initializes the WebDriver before each test and ensures
        proper cleanup after test execution.
        """
        logger.info("Setting up test environment")
        self.driver = get_driver()
        yield
        logger.info("Tearing down test environment")
        if self.driver:
            self.driver.quit()
    
    def take_screenshot(self, name):
        """Take a screenshot with the given name.
        
        Args:
            name (str): Name for the screenshot file
        """
        if self.driver:
            screenshot_path = f"screenshots/{name}.png"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
    
    def log_test_info(self, message):
        """Log test information.
        
        Args:
            message (str): Message to log
        """
        logger.info(message)
