"""Custom Exception Classes

Defines custom exceptions for the automation framework.
"""

import logging


logger = logging.getLogger(__name__)


class AutomationFrameworkException(Exception):
    """Base exception for automation framework."""
    
    def __init__(self, message: str):
        self.message = message
        logger.error(f"AutomationFrameworkException: {message}")
        super().__init__(self.message)


class ElementNotFoundException(AutomationFrameworkException):
    """Exception raised when an element is not found."""
    
    def __init__(self, locator: str):
        message = f"Element not found with locator: {locator}"
        super().__init__(message)


class PageLoadException(AutomationFrameworkException):
    """Exception raised when a page fails to load."""
    
    def __init__(self, page_name: str):
        message = f"Page failed to load: {page_name}"
        super().__init__(message)


class ConfigurationException(AutomationFrameworkException):
    """Exception raised for configuration errors."""
    
    def __init__(self, config_item: str):
        message = f"Configuration error: {config_item}"
        super().__init__(message)


class TestDataException(AutomationFrameworkException):
    """Exception raised for test data errors."""
    
    def __init__(self, data_key: str):
        message = f"Test data error: {data_key}"
        super().__init__(message)


class DriverException(AutomationFrameworkException):
    """Exception raised for WebDriver errors."""
    
    def __init__(self, driver_type: str):
        message = f"WebDriver error: {driver_type}"
        super().__init__(message)
