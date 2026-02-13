"""Pytest Configuration and Fixtures

Provides shared fixtures and configuration for all test modules.
"""

import pytest
import os
import logging
from datetime import datetime
from core.driver_factory import get_driver, quit_driver
from utils.logger import setup_logger


# Setup logging
logger = setup_logger(__name__)


@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance for each test.
    
    Yields:
        WebDriver: Configured WebDriver instance
    """
    logger.info("Initializing WebDriver")
    driver_instance = get_driver()
    yield driver_instance
    logger.info("Quitting WebDriver")
    quit_driver(driver_instance)


@pytest.fixture(scope="session")
def test_config():
    """Fixture to provide test configuration.
    
    Returns:
        dict: Test configuration dictionary
    """
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure.
    
    Args:
        item: Test item
        call: Test call
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get driver from fixture if available
        driver = None
        if hasattr(item, 'funcargs'):
            driver = item.funcargs.get('driver')
        
        if driver:
            # Create screenshots directory
            screenshot_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Take screenshot
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            try:
                driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to take screenshot: {str(e)}")


def pytest_configure(config):
    """Configure pytest with custom markers and settings.
    
    Args:
        config: Pytest config object
    """
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "ui: mark test as UI test")
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically.
    
    Args:
        config: Pytest config object
        items: List of collected test items
    """
    for item in items:
        # Auto-mark UI tests
        if "test_ui" in item.nodeid or "/ui/" in item.nodeid:
            item.add_marker(pytest.mark.ui)
        
        # Auto-mark API tests
        if "test_api" in item.nodeid or "/api/" in item.nodeid:
            item.add_marker(pytest.mark.api)
