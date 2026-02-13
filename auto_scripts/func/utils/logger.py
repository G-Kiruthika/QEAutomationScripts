"""Logging Utility Module

Provides centralized logging configuration and utilities
for the automation framework.
"""

import logging
import os
from datetime import datetime
import yaml


def setup_logger(name=None, log_file=None, level=None):
    """Setup and configure logger.
    
    Args:
        name (str, optional): Logger name. Defaults to root logger.
        log_file (str, optional): Log file path. Defaults to config value.
        level (str, optional): Log level. Defaults to config value or INFO.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            logging_config = config.get('logging', {})
    except FileNotFoundError:
        logging_config = {}
    
    # Determine log level
    level = level or logging_config.get('level', 'INFO')
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Determine log file
    if not log_file:
        log_file = logging_config.get('file', 'logs/test_execution.log')
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    
    # Formatter
    log_format = logging_config.get(
        'format',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    formatter = logging.Formatter(log_format)
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def log_test_start(test_name):
    """Log test execution start.
    
    Args:
        test_name (str): Name of the test
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info(f"Starting test: {test_name}")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)


def log_test_end(test_name, status):
    """Log test execution end.
    
    Args:
        test_name (str): Name of the test
        status (str): Test status (PASSED/FAILED)
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info(f"Test completed: {test_name}")
    logger.info(f"Status: {status}")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)


def log_step(step_description):
    """Log test step.
    
    Args:
        step_description (str): Description of the step
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Step: {step_description}")


def log_assertion(assertion_description, result):
    """Log assertion result.
    
    Args:
        assertion_description (str): Description of the assertion
        result (bool): Assertion result
    """
    logger = logging.getLogger(__name__)
    status = "PASSED" if result else "FAILED"
    logger.info(f"Assertion [{status}]: {assertion_description}")
