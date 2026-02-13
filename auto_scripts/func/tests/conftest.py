# tests/conftest.py
# Pytest configuration and fixtures for test suite

import pytest
import os
import yaml
from datetime import datetime
from core.driver_factory import get_driver


@pytest.fixture(scope="function")
def driver():
    """
    Fixture to provide WebDriver instance for each test
    Automatically handles driver cleanup after test execution
    """
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="session")
def config():
    """
    Fixture to load and provide configuration for test suite
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="function")
def test_data(config):
    """
    Fixture to provide test data from configuration
    """
    return config.get('test_data', {})


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test execution status and handle failures
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == 'call' and rep.failed:
        # Get driver from test if available
        if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
            driver = item.funcargs['driver']
            
            # Take screenshot on failure
            screenshot_dir = 'screenshots'
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            try:
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Failed to capture screenshot: {str(e)}")


def pytest_configure(config):
    """
    Configure pytest with custom markers and settings
    """
    config.addinivalue_line(
        "markers", "ui: mark test as UI automation test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API automation test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "login: mark test as login feature test"
    )