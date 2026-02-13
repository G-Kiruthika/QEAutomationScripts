"""Custom Exceptions Module

This module defines custom exceptions for the automation framework.
"""


class AutomationFrameworkException(Exception):
    """Base exception for automation framework."""
    pass


class PageLoadException(AutomationFrameworkException):
    """Exception raised when a page fails to load."""
    
    def __init__(self, page_name, message="Page failed to load"):
        self.page_name = page_name
        self.message = f"{message}: {page_name}"
        super().__init__(self.message)


class ElementNotFoundException(AutomationFrameworkException):
    """Exception raised when an element is not found."""
    
    def __init__(self, locator, message="Element not found"):
        self.locator = locator
        self.message = f"{message}: {locator}"
        super().__init__(self.message)


class ElementNotInteractableException(AutomationFrameworkException):
    """Exception raised when an element is not interactable."""
    
    def __init__(self, locator, message="Element not interactable"):
        self.locator = locator
        self.message = f"{message}: {locator}"
        super().__init__(self.message)


class TimeoutException(AutomationFrameworkException):
    """Exception raised when an operation times out."""
    
    def __init__(self, operation, timeout, message="Operation timed out"):
        self.operation = operation
        self.timeout = timeout
        self.message = f"{message}: {operation} after {timeout} seconds"
        super().__init__(self.message)


class ConfigurationException(AutomationFrameworkException):
    """Exception raised for configuration-related errors."""
    
    def __init__(self, config_key, message="Configuration error"):
        self.config_key = config_key
        self.message = f"{message}: {config_key}"
        super().__init__(self.message)


class DataNotFoundException(AutomationFrameworkException):
    """Exception raised when test data is not found."""
    
    def __init__(self, data_key, message="Test data not found"):
        self.data_key = data_key
        self.message = f"{message}: {data_key}"
        super().__init__(self.message)


class APIException(AutomationFrameworkException):
    """Exception raised for API-related errors."""
    
    def __init__(self, endpoint, status_code, message="API request failed"):
        self.endpoint = endpoint
        self.status_code = status_code
        self.message = f"{message}: {endpoint} (Status: {status_code})"
        super().__init__(self.message)


class ValidationException(AutomationFrameworkException):
    """Exception raised for validation errors."""
    
    def __init__(self, expected, actual, message="Validation failed"):
        self.expected = expected
        self.actual = actual
        self.message = f"{message}: Expected '{expected}', but got '{actual}'"
        super().__init__(self.message)
