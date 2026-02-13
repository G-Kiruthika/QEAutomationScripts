# utils/logger.py

import logging
import os
from datetime import datetime
import yaml


def setup_logger(name=__name__, log_file=None, level=logging.INFO):
    """
    Set up and configure logger for test automation.
    
    Args:
        name (str): Logger name
        log_file (str): Path to log file (optional)
        level: Logging level
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        log_config = config.get('logging', {})
        level_str = log_config.get('level', 'INFO')
        level = getattr(logging, level_str, logging.INFO)
        log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file = log_file or log_config.get('file', 'logs/test_execution.log')
    except (FileNotFoundError, KeyError):
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        log_file = log_file or 'logs/test_execution.log'
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatters
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name=__name__):
    """
    Get or create a logger instance.
    
    Args:
        name (str): Logger name
    
    Returns:
        logging.Logger: Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger