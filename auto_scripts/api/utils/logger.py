"""Logging utility for test framework.

Provides centralized logging functionality for all test components.
"""

import logging
import os
from datetime import datetime


class TestLogger:
    """Custom logger class for test automation framework."""
    
    def __init__(self, name=__name__, log_level=logging.INFO):
        """Initialize logger with specified name and level.
        
        Args:
            name (str): Logger name
            log_level (int): Logging level (default: INFO)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create file handler with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'test_execution_{timestamp}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info level message."""
        self.logger.info(message)
    
    def debug(self, message):
        """Log debug level message."""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log warning level message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error level message."""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical level message."""
        self.logger.critical(message)


# Global logger instance
logger = TestLogger()
