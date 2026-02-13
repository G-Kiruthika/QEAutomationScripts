# tests/conftest.py

import pytest
from core.driver_factory import get_driver, quit_driver
import yaml
import os
from datetime import datetime

@pytest.fixture(scope="function")
def driver():
    """
    Fixture to provide WebDriver instance for each test
    
    Yields:
        WebDriver: Configured WebDriver instance
    """
    driver_instance = get_driver()
    yield driver_instance
    quit_driver(driver_instance)

@pytest.fixture(scope="session")
def config():
    """
    Fixture to load and provide configuration
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path) as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def base_url(config):
    """
    Fixture to provide base URL from configuration
    
    Args:
        config: Configuration fixture
    
    Returns:
        str: Base URL
    """
    return config['ui']['base_url']

@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """
    Session-level setup and teardown
    """
    print("\n=== Test Session Started ===")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    yield
    
    print("\n=== Test Session Completed ===")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and perform actions on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get driver from test if available
        driver = None
        if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
            driver = item.funcargs['driver']
        
        # Take screenshot on failure
        if driver:
            try:
                screenshot_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
                os.makedirs(screenshot_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_name = f"{item.name}_{timestamp}.png"
                screenshot_path = os.path.join(screenshot_dir, screenshot_name)
                
                driver.save_screenshot(screenshot_path)
                print(f"\nScreenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"\nFailed to capture screenshot: {str(e)}")

def pytest_configure(config):
    """
    Configure pytest with custom markers
    """
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "ui: mark test as UI test")
    config.addinivalue_line("markers", "api: mark test as API test")
