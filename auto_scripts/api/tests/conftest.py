"""Pytest configuration file for test fixtures and hooks.

This file contains shared fixtures and configuration for all tests.
"""

import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture(scope="function")
def driver(request):
    """WebDriver fixture that initializes and tears down browser driver.
    
    Returns:
        WebDriver: Selenium WebDriver instance
    """
    # Load configuration
    try:
        with open('auto_scripts/api/config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        config = {
            'browser': 'chrome',
            'headless': False,
            'base_url': 'http://localhost:8080'
        }
    
    browser = config.get('browser', 'chrome').lower()
    headless = config.get('headless', False)
    
    # Initialize driver based on browser type
    if browser == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    # Navigate to base URL if configured
    base_url = config.get('base_url')
    if base_url:
        driver.get(base_url)
    
    yield driver
    
    # Teardown
    driver.quit()


@pytest.fixture(scope="session")
def config():
    """Load and provide test configuration.
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open('auto_scripts/api/config/config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            'browser': 'chrome',
            'headless': False,
            'base_url': 'http://localhost:8080'
        }
