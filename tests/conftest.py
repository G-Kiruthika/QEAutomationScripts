import pytest
import yaml
import os
from core.driver_factory import get_driver
from utils.send_email_report import send_email_report

@pytest.fixture(scope="session")
def config():
    """Load configuration for test session"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="function")
def driver():
    """Create WebDriver instance for each test"""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()

def pytest_sessionfinish(session, exitstatus):
    """Hook to run after all tests complete"""
    # Collect test results
    test_results = {
        'total': session.testscollected,
        'passed': session.testscollected - session.testsfailed,
        'failed': session.testsfailed,
        'skipped': 0,
        'failed_tests': []
    }
    
    # Send email report
    send_email_report(test_results)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Log failed test
        print(f"Test failed: {item.nodeid}")