# Pytest Configuration and Fixtures for EcommerceLoginFlow Suite
import pytest
import logging
from core.driver_factory import get_driver
from core.test_data_loader import TestDataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.fixture(scope='function')
def driver():
    """Fixture to provide WebDriver instance for each test."""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()

@pytest.fixture(scope='session')
def test_config():
    """Fixture to provide test configuration."""
    config = TestDataLoader.load_yaml_config()
    return config

@pytest.fixture(scope='function')
def valid_user_credentials():
    """Fixture to provide valid user credentials."""
    return TestDataLoader.get_test_user('valid_user')

@pytest.fixture(scope='function')
def invalid_user_credentials():
    """Fixture to provide invalid user credentials."""
    return TestDataLoader.get_test_user('invalid_user')
