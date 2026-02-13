import pytest
from auto_scripts.core.driver_factory import get_driver
import yaml
import os


@pytest.fixture(scope="session")
def config():
    """
    Load and provide test configuration
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = 'auto_scripts/api/config/config.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="function")
def driver(config):
    """
    Provide WebDriver instance for tests
    
    Args:
        config (dict): Test configuration
    
    Yields:
        WebDriver: Configured WebDriver instance
    """
    browser = config.get('ui', {}).get('browser', 'chrome')
    headless = config.get('ui', {}).get('headless', False)
    
    driver_instance = get_driver(browser=browser, headless=headless)
    
    yield driver_instance
    
    driver_instance.quit()


@pytest.fixture(scope="function")
def test_data(config):
    """
    Provide test data from configuration
    
    Args:
        config (dict): Test configuration
    
    Returns:
        dict: Test data dictionary
    """
    return config.get('test_data', {})


def pytest_configure(config):
    """
    Pytest configuration hook
    Create necessary directories
    """
    # Create logs directory
    log_dir = "auto_scripts/api/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create screenshots directory
    screenshot_dir = "auto_scripts/api/screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get driver from fixture if available
        driver = item.funcargs.get('driver')
        if driver:
            screenshot_dir = "auto_scripts/api/screenshots"
            screenshot_name = f"{item.name}_{report.when}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
