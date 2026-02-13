"""Pytest configuration and fixtures for test suite"""
import pytest
from core.driver_factory import get_driver
import yaml

@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance for tests"""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()

@pytest.fixture(scope="session")
def config():
    """Fixture to load configuration from config.yaml"""
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="function")
def test_data(config):
    """Fixture to provide test data from configuration"""
    return config.get('test_data', {})

def pytest_configure(config):
    """Pytest configuration hook"""
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "registration: mark test as registration feature test"
    )
    config.addinivalue_line(
        "markers", "database: mark test as database validation test"
    )
