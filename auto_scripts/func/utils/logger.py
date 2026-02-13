"""Logger Utility Module

This module provides logging configuration and utilities for the automation framework.
"""

import os
import logging
from datetime import datetime


def setup_logger(name=__name__, log_level=logging.INFO, log_file=None):
    """Set up and configure a logger.
    
    Args:
        name (str): Logger name. Defaults to module name.
        log_level (int): Logging level. Defaults to INFO.
        log_file (str, optional): Path to log file. If None, logs to console only.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file is provided)
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name=__name__):
    """Get or create a logger instance.
    
    Args:
        name (str): Logger name. Defaults to module name.
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


class TestLogger:
    """Test-specific logger with enhanced functionality."""
    
    def __init__(self, test_name, log_dir='logs'):
        """Initialize TestLogger.
        
        Args:
            test_name (str): Name of the test
            log_dir (str): Directory to store log files
        """
        self.test_name = test_name
        self.log_dir = log_dir
        
        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f"{test_name}_{timestamp}.log")
        
        self.logger = setup_logger(
            name=test_name,
            log_level=logging.DEBUG,
            log_file=log_file
        )
    
    def info(self, message):
        """Log info message."""
        self.logger.info(message)
    
    def debug(self, message):
        """Log debug message."""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message."""
        self.logger.critical(message)
    
    def step(self, step_number, description):
        """Log test step.
        
        Args:
            step_number (int): Step number
            description (str): Step description
        """
        self.logger.info(f"STEP {step_number}: {description}")
    
    def result(self, passed, message=""):
        """Log test result.
        
        Args:
            passed (bool): Whether test passed
            message (str): Additional message
        """
        status = "PASSED" if passed else "FAILED"
        log_method = self.logger.info if passed else self.logger.error
        log_method(f"TEST {status}: {self.test_name} - {message}")
