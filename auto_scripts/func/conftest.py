import pytest
import os
import yaml
from datetime import datetime
from core.driver_factory import get_driver
from core.error_handler import ErrorHandler


# Initialize error handler
error_handler = ErrorHandler()


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="session")
def config():
    """Session-scoped fixture to load configuration"""
    return load_config()


@pytest.fixture(scope="function")
def driver(config):
    """Function-scoped fixture to provide WebDriver instance"""
    browser = config.get('browser', 'chrome')
    headless = config.get('headless', False)
    
    error_handler.log_info(f"Initializing {browser} driver (headless={headless})")
    driver_instance = get_driver(browser=browser, headless=headless)
    
    yield driver_instance
    
    error_handler.log_info("Closing driver")
    driver_instance.quit()


@pytest.fixture(scope="function", autouse=True)
def test_logger(request):
    """Auto-use fixture to log test execution"""
    test_name = request.node.name
    error_handler.log_info(f"Starting test: {test_name}")
    
    yield
    
    error_handler.log_info(f"Completed test: {test_name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and handle failures"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get driver from fixture if available
        driver_fixture = None
        if 'driver' in item.fixturenames:
            driver_fixture = item.funcargs.get('driver')
        
        # Handle test failure
        error_handler.handle_test_failure(
            test_name=item.name,
            error=call.excinfo.value if call.excinfo else Exception("Test failed"),
            driver=driver_fixture
        )


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Session-scoped fixture to setup test environment"""
    error_handler.log_info("Setting up test environment")
    
    # Create necessary directories
    directories = ['logs', 'logs/screenshots', 'reports', 'reports/allure-results']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    yield
    
    error_handler.log_info("Tearing down test environment")


@pytest.fixture(scope="function")
def base_url(config):
    """Fixture to provide base URL based on environment"""
    env = config.get('default_environment', 'qa')
    environments = config.get('environments', {})
    return environments.get(env, {}).get('base_url', 'https://ecommerce-website.com')


@pytest.fixture(scope="function")
def test_data(config):
    """Fixture to provide test data"""
    return config.get('test_data', {})
