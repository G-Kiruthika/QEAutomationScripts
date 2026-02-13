# tests/conftest.py

import pytest
from core.driver_factory import get_driver
from utils.logger import setup_logger, log_test_start, log_test_end
import os


# Setup logger
logger = setup_logger()


@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to provide WebDriver instance for each test
    """
    driver = get_driver()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and log them
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        test_name = item.nodeid
        if report.passed:
            log_test_end(logger, test_name, "PASSED")
        elif report.failed:
            log_test_end(logger, test_name, "FAILED")
            logger.error(f"Error: {report.longreprtext}")


@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):
    """
    Automatically log test start for each test
    """
    test_name = request.node.nodeid
    log_test_start(logger, test_name)
    yield


@pytest.fixture(scope="session")
def test_config():
    """
    Load and provide test configuration
    """
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config
