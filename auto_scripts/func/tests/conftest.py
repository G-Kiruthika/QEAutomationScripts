"""Pytest Configuration File

Provides fixtures and hooks for test execution.
"""

import pytest
from core.driver_factory import get_driver
import logging
import os
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance for each test
    
    Yields:
        WebDriver: Selenium WebDriver instance
    """
    driver = get_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def config():
    """Fixture to load configuration
    
    Returns:
        dict: Configuration dictionary
    """
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            screenshot_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot saved: {screenshot_path}")
