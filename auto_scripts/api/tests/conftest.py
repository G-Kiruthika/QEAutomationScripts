# Pytest configuration file
# Contains fixtures and hooks for test execution

import pytest
from auto_scripts.core.driver_factory import get_driver
import yaml
import os


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def config():
    """Fixture to provide configuration to tests"""
    return load_config()


@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance"""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="function")
def base_url(config):
    """Fixture to provide base URL"""
    return config['ui']['base_url']


def pytest_configure(config):
    """Pytest configuration hook"""
    # Add custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "ui: mark test as UI test")
    config.addinivalue_line("markers", "api: mark test as API test")


def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    if call.when == "call":
        if call.excinfo is not None:
            # Test failed
            print(f"Test {item.name} failed: {call.excinfo.value}")
