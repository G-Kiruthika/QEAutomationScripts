"""Pytest Configuration and Fixtures

Provides shared fixtures and configuration for test execution.
"""

import pytest
import logging
import os
from datetime import datetime
from core.driver_factory import get_driver, quit_driver
from utils.logger import setup_logger, log_test_start, log_test_end

# Setup logger
logger = setup_logger(__name__)


@pytest.fixture(scope="session")
def setup_logging():
    """Setup logging for test session."""
    logger.info("Test session started")
    yield
    logger.info("Test session completed")


@pytest.fixture(scope="function")
def driver(request):
    """Provide WebDriver instance for tests.
    
    Args:
        request: Pytest request object
    
    Yields:
        WebDriver: Configured WebDriver instance
    """
    test_name = request.node.name
    log_test_start(test_name)
    
    driver_instance = get_driver()
    
    yield driver_instance
    
    # Capture screenshot on failure
    if request.node.rep_call.failed:
        try:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
            driver_instance.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
    
    status = "PASSED" if not request.node.rep_call.failed else "FAILED"
    log_test_end(test_name, status)
    
    quit_driver(driver_instance)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def test_config():
    """Load and provide test configuration.
    
    Returns:
        dict: Test configuration
    """
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info("Test configuration loaded successfully")
        return config
    except FileNotFoundError:
        logger.warning(f"Config file not found: {config_path}")
        return {}


def pytest_configure(config):
    """Configure pytest with custom markers."""
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
