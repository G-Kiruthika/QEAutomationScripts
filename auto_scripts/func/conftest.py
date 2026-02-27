import pytest
import os
import yaml
from datetime import datetime
from core.driver_factory import get_driver
from utils.send_email_report import send_test_failure_report, send_test_summary_report

# Global test results tracking
test_results = []

def load_config():
    """Load configuration from config.yaml."""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

@pytest.fixture(scope="session")
def config():
    """Provide configuration data to tests."""
    return load_config()

@pytest.fixture(scope="function")
def driver(config):
    """Provide WebDriver instance for tests."""
    browser_config = config.get('ui', {}).get('browser', {})
    browser = browser_config.get('default', 'chrome')
    headless = browser_config.get('headless', False)
    
    driver_instance = get_driver(browser=browser, headless=headless)
    yield driver_instance
    driver_instance.quit()

@pytest.fixture(scope="function")
def test_data(config):
    """Provide test data from configuration."""
    return config.get('ui', {}).get('test_users', {})

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for reporting."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        test_result = {
            'name': item.name,
            'passed': report.passed,
            'failed': report.failed,
            'skipped': report.skipped,
            'duration': report.duration,
            'timestamp': datetime.now().isoformat()
        }
        
        if report.failed:
            test_result['error'] = str(report.longrepr)
            
            # Send failure notification if enabled
            config = load_config()
            email_config = config.get('email', {})
            if email_config.get('enabled', False) and email_config.get('send_on_failure', False):
                send_test_failure_report(
                    test_name=item.name,
                    error_message=str(report.longrepr)
                )
        
        test_results.append(test_result)

def pytest_sessionfinish(session, exitstatus):
    """Hook called after test session finishes."""
    if test_results:
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r['passed']])
        failed_tests = len([r for r in test_results if r['failed']])
        
        # Send summary report if enabled
        config = load_config()
        email_config = config.get('email', {})
        if email_config.get('enabled', False) and email_config.get('send_summary', False):
            send_test_summary_report(
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                test_results=test_results
            )

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests."""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create screenshots directory if it doesn't exist
    screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)
    
    yield
    
    # Cleanup after all tests
    print(f"\nTest execution completed. Total results: {len(test_results)}")

@pytest.fixture
def take_screenshot(driver, request):
    """Fixture to take screenshot on test failure."""
    yield
    
    if request.node.rep_call.failed:
        config = load_config()
        execution_config = config.get('execution', {})
        
        if execution_config.get('screenshot_on_failure', True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{request.node.name}_{timestamp}.png"
            screenshot_path = os.path.join(
                os.path.dirname(__file__), 
                'screenshots', 
                screenshot_name
            )
            
            try:
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Failed to take screenshot: {str(e)}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """Hook to setup individual test runs."""
    yield

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Hook called during test execution."""
    outcome = yield
    
    # Store the test result in the item for later use
    item.rep_call = outcome.get_result()

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )