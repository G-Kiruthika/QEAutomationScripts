import logging
import traceback
from datetime import datetime
import os


class ErrorHandler:
    """Centralized error handling and logging"""

    def __init__(self, log_dir: str = None):
        """Initialize ErrorHandler with optional log directory"""
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Setup logger
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Setup logging configuration"""
        logger = logging.getLogger('AutomationFramework')
        logger.setLevel(logging.DEBUG)
        
        # Create file handler
        log_file = os.path.join(self.log_dir, f'automation_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

    def log_error(self, error: Exception, context: str = ""):
        """Log error with traceback"""
        error_msg = f"Error in {context}: {str(error)}" if context else f"Error: {str(error)}"
        self.logger.error(error_msg)
        self.logger.error(traceback.format_exc())

    def log_info(self, message: str):
        """Log info message"""
        self.logger.info(message)

    def log_warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)

    def log_debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)

    def handle_test_failure(self, test_name: str, error: Exception, driver=None):
        """Handle test failure with screenshot capture"""
        self.log_error(error, f"Test: {test_name}")
        
        if driver:
            try:
                screenshot_dir = os.path.join(self.log_dir, 'screenshots')
                os.makedirs(screenshot_dir, exist_ok=True)
                
                screenshot_path = os.path.join(
                    screenshot_dir,
                    f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                driver.save_screenshot(screenshot_path)
                self.logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as screenshot_error:
                self.logger.error(f"Failed to capture screenshot: {str(screenshot_error)}")

    def handle_assertion_error(self, expected, actual, message: str = ""):
        """Handle assertion errors with detailed logging"""
        error_msg = f"Assertion Failed: {message}\n" if message else "Assertion Failed:\n"
        error_msg += f"Expected: {expected}\n"
        error_msg += f"Actual: {actual}"
        self.logger.error(error_msg)
        raise AssertionError(error_msg)
