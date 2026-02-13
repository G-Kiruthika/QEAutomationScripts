# utils/logger.py

import logging
import os
from datetime import datetime
import yaml


def load_config():
    """
    Load configuration from config.yaml
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def setup_logger(name: str = 'automation_framework'):
    """
    Setup and configure logger
    
    Args:
        name (str): Logger name
    
    Returns:
        logging.Logger: Configured logger instance
    """
    config = load_config()
    log_level = config.get('logging', {}).get('level', 'INFO')
    log_file = config.get('logging', {}).get('log_file', 'logs/automation.log')
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def log_test_start(logger, test_name: str):
    """
    Log test start
    
    Args:
        logger: Logger instance
        test_name (str): Name of the test
    """
    logger.info(f"{'='*80}")
    logger.info(f"Starting test: {test_name}")
    logger.info(f"{'='*80}")


def log_test_end(logger, test_name: str, status: str):
    """
    Log test end
    
    Args:
        logger: Logger instance
        test_name (str): Name of the test
        status (str): Test status (PASSED/FAILED)
    """
    logger.info(f"{'='*80}")
    logger.info(f"Test {test_name} - {status}")
    logger.info(f"{'='*80}")


def log_step(logger, step_number: int, description: str):
    """
    Log test step
    
    Args:
        logger: Logger instance
        step_number (int): Step number
        description (str): Step description
    """
    logger.info(f"Step {step_number}: {description}")
