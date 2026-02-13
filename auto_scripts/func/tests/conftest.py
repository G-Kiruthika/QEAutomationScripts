"""Pytest Configuration and Fixtures

This module contains pytest configuration and shared fixtures
for the automation test suite.
"""

import os
import pytest
import logging
from datetime import datetime
from core.driver_factory import get_driver, quit_driver
from utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__, log_level=logging.INFO)


def pytest_configure(config):
    """Pytest configuration hook."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create screenshots directory if it doesn't exist
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    
    logger.info("Pytest configuration completed")


@pytest.fixture(scope="function")
def driver(request):
    """Fixture to provide WebDriver instance for tests.
    
    Args:
        request: Pytest request object
    
    Yields:
        WebDriver: Configured WebDriver instance
    """
    logger.info(f"Setting up driver for test: {request.node.name}")
    driver_instance = get_driver()
    
    yield driver_instance
    
    # Teardown: Take screenshot on failure and quit driver
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"screenshots/{request.node.name}_{timestamp}.png"
        driver_instance.save_screenshot(screenshot_name)
        logger.error(f"Test failed. Screenshot saved: {screenshot_name}")
    
    logger.info(f"Tearing down driver for test: {request.node.name}")
    quit_driver(driver_instance)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to make test result available in fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def test_config():
    """Fixture to provide test configuration.
    
    Returns:
        dict: Test configuration dictionary
    """
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
            logger.info("Test configuration loaded")
            return config
    else:
        logger.warning("Config file not found, using default configuration")
        return {}


@pytest.fixture(scope="function")
def test_logger(request):
    """Fixture to provide test-specific logger.
    
    Args:
        request: Pytest request object
    
    Returns:
        logging.Logger: Test-specific logger
    """
    test_name = request.node.name
    test_logger_instance = setup_logger(
        name=test_name,
        log_level=logging.DEBUG,
        log_file=f"logs/{test_name}.log"
    )
    return test_logger_instance


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment to run tests: dev, test, staging, prod"
    )


@pytest.fixture(scope="session")
def browser(request):
    """Fixture to get browser from command line."""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    """Fixture to get headless mode from command line."""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def env(request):
    """Fixture to get environment from command line."""
    return request.config.getoption("--env")
