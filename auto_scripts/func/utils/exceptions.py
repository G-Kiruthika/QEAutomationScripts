"""Custom exceptions for the automation framework"""


class AutomationFrameworkException(Exception):
    """Base exception for automation framework"""
    pass


class ElementNotFoundException(AutomationFrameworkException):
    """Exception raised when element is not found"""
    
    def __init__(self, locator, message="Element not found"):
        self.locator = locator
        self.message = f"{message}: {locator}"
        super().__init__(self.message)


class ElementNotClickableException(AutomationFrameworkException):
    """Exception raised when element is not clickable"""
    
    def __init__(self, locator, message="Element not clickable"):
        self.locator = locator
        self.message = f"{message}: {locator}"
        super().__init__(self.message)


class ElementNotVisibleException(AutomationFrameworkException):
    """Exception raised when element is not visible"""
    
    def __init__(self, locator, message="Element not visible"):
        self.locator = locator
        self.message = f"{message}: {locator}"
        super().__init__(self.message)


class PageLoadException(AutomationFrameworkException):
    """Exception raised when page fails to load"""
    
    def __init__(self, url, message="Page failed to load"):
        self.url = url
        self.message = f"{message}: {url}"
        super().__init__(self.message)


class TestDataException(AutomationFrameworkException):
    """Exception raised for test data related errors"""
    
    def __init__(self, data_key, message="Test data error"):
        self.data_key = data_key
        self.message = f"{message}: {data_key}"
        super().__init__(self.message)


class ConfigurationException(AutomationFrameworkException):
    """Exception raised for configuration related errors"""
    
    def __init__(self, config_key, message="Configuration error"):
        self.config_key = config_key
        self.message = f"{message}: {config_key}"
        super().__init__(self.message)


class DriverException(AutomationFrameworkException):
    """Exception raised for WebDriver related errors"""
    
    def __init__(self, driver_type, message="Driver error"):
        self.driver_type = driver_type
        self.message = f"{message}: {driver_type}"
        super().__init__(self.message)
