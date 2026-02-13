# utils/exception_handler.py

import logging
import traceback
from functools import wraps


class AutomationException(Exception):
    """Base exception class for automation framework."""
    pass


class ElementNotFoundException(AutomationException):
    """Exception raised when an element is not found."""
    pass


class TimeoutException(AutomationException):
    """Exception raised when an operation times out."""
    pass


class PageLoadException(AutomationException):
    """Exception raised when a page fails to load."""
    pass


class ValidationException(AutomationException):
    """Exception raised when validation fails."""
    pass


class ConfigurationException(AutomationException):
    """Exception raised for configuration errors."""
    pass


def handle_exceptions(logger=None):
    """
    Decorator to handle exceptions in test methods.
    
    Args:
        logger: Logger instance (optional)
    
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log = logger or logging.getLogger(func.__module__)
            try:
                return func(*args, **kwargs)
            except AutomationException as e:
                log.error(f"Automation error in {func.__name__}: {str(e)}")
                log.debug(traceback.format_exc())
                raise
            except Exception as e:
                log.error(f"Unexpected error in {func.__name__}: {str(e)}")
                log.debug(traceback.format_exc())
                raise AutomationException(f"Unexpected error: {str(e)}") from e
        return wrapper
    return decorator


def log_exception(exception, logger=None, context=""):
    """
    Log an exception with context.
    
    Args:
        exception: Exception instance
        logger: Logger instance (optional)
        context (str): Additional context information
    """
    log = logger or logging.getLogger(__name__)
    
    error_msg = f"{context}: {type(exception).__name__} - {str(exception)}" if context else f"{type(exception).__name__} - {str(exception)}"
    
    log.error(error_msg)
    log.debug(traceback.format_exc())


def assert_with_logging(condition, message, logger=None):
    """
    Assert with logging on failure.
    
    Args:
        condition: Condition to assert
        message (str): Error message if assertion fails
        logger: Logger instance (optional)
    
    Raises:
        ValidationException: If condition is False
    """
    log = logger or logging.getLogger(__name__)
    
    if not condition:
        log.error(f"Assertion failed: {message}")
        raise ValidationException(message)
    else:
        log.info(f"Assertion passed: {message}")