"""Custom Exceptions Module

Defines custom exception classes for the automation framework.
"""


class AutomationFrameworkException(Exception):
    """Base exception for automation framework."""
    pass


class ElementNotFoundException(AutomationFrameworkException):
    """Raised when an element cannot be found."""
    pass


class ElementNotVisibleException(AutomationFrameworkException):
    """Raised when an element is not visible."""
    pass


class ElementNotClickableException(AutomationFrameworkException):
    """Raised when an element is not clickable."""
    pass


class PageLoadException(AutomationFrameworkException):
    """Raised when a page fails to load."""
    pass


class ConfigurationException(AutomationFrameworkException):
    """Raised when there's a configuration error."""
    pass


class TestDataException(AutomationFrameworkException):
    """Raised when there's an issue with test data."""
    pass


class DriverException(AutomationFrameworkException):
    """Raised when there's an issue with WebDriver."""
    pass
