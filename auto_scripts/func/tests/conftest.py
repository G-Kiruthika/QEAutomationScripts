"""Pytest configuration and fixtures"""

import pytest
import logging
import os
from datetime import datetime
from core.driver_factory import get_driver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def setup_test_environment():
    """Setup test environment before test session"""
    logger.info("Setting up test environment")
    
    # Create necessary directories
    directories = ['logs', 'screenshots', 'reports']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
    
    yield
    
    logger.info("Test environment cleanup completed")


@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance"""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        # Take screenshot on test failure
        driver = item.funcargs.get('driver')
        if driver:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{item.name}_{timestamp}"
            screenshot_path = f"screenshots/{screenshot_name}.png"
            try:
                driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to take screenshot: {str(e)}")


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
