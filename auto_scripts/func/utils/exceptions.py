"""Custom Exceptions Module

Defines custom exception classes for the automation framework.
"""


class AutomationFrameworkException(Exception):
    """Base exception for automation framework."""
    pass


class PageLoadException(AutomationFrameworkException):
    """Raised when page fails to load properly."""
    
    def __init__(self, page_name, message="Page failed to load"):
        self.page_name = page_name
        self.message = f"{message}: {page_name}"
        super().__init__(self.message)


class ElementNotFoundException(AutomationFrameworkException):
    """Raised when element cannot be found."""
    
    def __init__(self, locator, message="Element not found"):
        self.locator = locator
        self.message = f"{message}: {locator}"
        super().__init__(self.message)


class ElementNotInteractableException(AutomationFrameworkException):
    """Raised when element is not interactable."""
    
    def __init__(self, locator, message="Element not interactable"):
        self.locator = locator
        self.message = f"{message}: {locator}"
        super().__init__(self.message)


class ConfigurationException(AutomationFrameworkException):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, config_key, message="Configuration error"):
        self.config_key = config_key
        self.message = f"{message}: {config_key}"
        super().__init__(self.message)


class TestDataException(AutomationFrameworkException):
    """Raised when test data is invalid or missing."""
    
    def __init__(self, data_key, message="Test data error"):
        self.data_key = data_key
        self.message = f"{message}: {data_key}"
        super().__init__(self.message)


class APIException(AutomationFrameworkException):
    """Raised when API call fails."""
    
    def __init__(self, endpoint, status_code, message="API call failed"):
        self.endpoint = endpoint
        self.status_code = status_code
        self.message = f"{message}: {endpoint} (Status: {status_code})"
        super().__init__(self.message)


class ValidationException(AutomationFrameworkException):
    """Raised when validation fails."""
    
    def __init__(self, expected, actual, message="Validation failed"):
        self.expected = expected
        self.actual = actual
        self.message = f"{message}: Expected '{expected}', but got '{actual}'"
        super().__init__(self.message)
