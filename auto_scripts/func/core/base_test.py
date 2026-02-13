"""Base Test class with common test setup and teardown"""

import pytest
import logging
from core.driver_factory import get_driver

logger = logging.getLogger(__name__)


class BaseTest:
    """Base class for all test classes"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method executed before each test"""
        logger.info("Setting up test")
        self.driver = get_driver()
        yield
        logger.info("Tearing down test")
        self.driver.quit()
    
    def take_screenshot(self, name):
        """Take screenshot with given name"""
        try:
            screenshot_path = f"screenshots/{name}.png"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return None
    
    def log_test_info(self, message):
        """Log test information"""
        logger.info(message)
    
    def log_test_error(self, message):
        """Log test error"""
        logger.error(message)
