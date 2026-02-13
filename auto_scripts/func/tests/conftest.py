# tests/conftest.py

import pytest
from core.driver_factory import get_driver
from utils.screenshot_helper import take_screenshot_on_failure
import yaml
import os


@pytest.fixture(scope='function')
def driver():
    """Fixture to initialize and quit WebDriver for each test"""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope='session')
def config():
    """Fixture to load configuration"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test failures and take screenshots"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        # Get driver from test if available
        if 'driver' in item.funcargs:
            driver = item.funcargs['driver']
            test_name = item.nodeid.split('::')[-1]
            screenshot_path = take_screenshot_on_failure(driver, test_name)
            print(f"\nScreenshot saved: {screenshot_path}")
