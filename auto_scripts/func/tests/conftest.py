import pytest
from core.driver_factory import get_driver
import os
import yaml


@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to provide WebDriver instance for each test
    """
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="session")
def config():
    """
    Pytest fixture to load and provide configuration
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="function")
def login_page(driver):
    """
    Pytest fixture to provide LoginPage instance
    """
    from pages.login_page import LoginPage
    return LoginPage(driver)


def pytest_configure(config):
    """
    Pytest configuration hook
    """
    # Add custom markers
    config.addinivalue_line(
        "markers", "login: mark test as login functionality test"
    )
    config.addinivalue_line(
        "markers", "validation: mark test as validation test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as security test"
    )


def pytest_html_report_title(report):
    """
    Customize HTML report title
    """
    report.title = "Login Functionality Test Report"
