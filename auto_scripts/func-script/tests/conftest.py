import pytest
import os
import yaml
from datetime import datetime
from core.driver_factory import get_driver
from utils.send_email_report import send_test_completion_report


@pytest.fixture(scope="session")
def config():
    """Load configuration for test session"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="function")
def driver(config):
    """Create WebDriver instance for each test function"""
    driver_instance = get_driver()
    yield driver_instance
    
    # Cleanup
    if config['execution']['browser_cleanup']:
        driver_instance.quit()


@pytest.fixture(scope="function")
def take_screenshot_on_failure(request, driver):
    """Take screenshot on test failure"""
    yield
    
    if request.node.rep_call.failed:
        # Create screenshots directory if it doesn't exist
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Generate screenshot filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
        
        # Take screenshot
        try:
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for reporting"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session", autouse=True)
def test_session_setup_teardown(config):
    """Setup and teardown for entire test session"""
    # Session setup
    print("\n=== Test Session Started ===")
    start_time = datetime.now()
    
    # Store test results for reporting
    test_results = []
    
    yield test_results
    
    # Session teardown
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n=== Test Session Completed ===")
    print(f"Duration: {duration}")
    
    # Send email report if enabled
    if config.get('reporting', {}).get('email_notification', False):
        try:
            send_test_completion_report(test_results)
        except Exception as e:
            print(f"Failed to send email report: {str(e)}")


@pytest.fixture(autouse=True)
def collect_test_results(request, test_session_setup_teardown):
    """Collect test results for reporting"""
    test_results = test_session_setup_teardown
    
    yield
    
    # Collect test result after test execution
    if hasattr(request.node, 'rep_call'):
        result = {
            'test_name': request.node.name,
            'status': 'PASSED' if request.node.rep_call.passed else 'FAILED',
            'duration': f"{request.node.rep_call.duration:.2f}s" if hasattr(request.node.rep_call, 'duration') else 'N/A',
            'error_message': str(request.node.rep_call.longrepr) if request.node.rep_call.failed else ''
        }
        test_results.append(result)


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "registration: mark test as registration related"
    )
    config.addinivalue_line(
        "markers", "validation: mark test as validation test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names"""
    for item in items:
        # Add markers based on test file location
        if "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)
        if "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        
        # Add markers based on test name patterns
        if "smoke" in item.name or "basic" in item.name:
            item.add_marker(pytest.mark.smoke)
        if "registration" in item.name:
            item.add_marker(pytest.mark.registration)