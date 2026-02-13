"""Pytest configuration and fixtures for the automation framework.

This module contains shared fixtures and hooks for test execution.
"""

import pytest
import os
from datetime import datetime
from pathlib import Path
from core.driver_factory import get_driver, quit_driver
from utils.logger import AutomationLogger


@pytest.fixture(scope='function')
def driver():
    """
    Fixture to provide a WebDriver instance for each test.
    
    Yields:
        WebDriver: Selenium WebDriver instance
    """
    driver_instance = get_driver()
    yield driver_instance
    quit_driver(driver_instance)


@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """
    Session-level fixture to set up the test environment.
    """
    # Create necessary directories
    base_dir = Path(__file__).parent.parent
    
    directories = [
        base_dir / 'logs',
        base_dir / 'reports',
        base_dir / 'screenshots',
        base_dir / 'allure-results'
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
    
    logger = AutomationLogger.get_logger('pytest_setup')
    logger.info("Test environment setup completed")
    
    yield
    
    logger.info("Test environment teardown completed")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test execution results and take screenshots on failure.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call':
        logger = AutomationLogger.get_logger('test_execution')
        
        if report.passed:
            AutomationLogger.log_test_end(item.name, 'PASSED')
        elif report.failed:
            AutomationLogger.log_test_end(item.name, 'FAILED')
            
            # Take screenshot on failure if driver is available
            if 'driver' in item.funcargs:
                driver = item.funcargs['driver']
                screenshot_dir = Path(__file__).parent.parent / 'screenshots'
                screenshot_path = screenshot_dir / f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                
                try:
                    driver.save_screenshot(str(screenshot_path))
                    logger.info(f"Screenshot saved: {screenshot_path}")
                except Exception as e:
                    logger.error(f"Failed to capture screenshot: {str(e)}")
        elif report.skipped:
            AutomationLogger.log_test_end(item.name, 'SKIPPED')


@pytest.fixture(scope='function', autouse=True)
def log_test_info(request):
    """
    Fixture to log test start information.
    """
    AutomationLogger.log_test_start(request.node.name)
    yield


def pytest_configure(config):
    """
    Pytest configuration hook.
    """
    # Add custom markers
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