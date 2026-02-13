# Logger utility for automation framework
# Provides centralized logging functionality

import logging
import os
from datetime import datetime
import yaml


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def setup_logger(name=__name__, log_file=None, level=None):
    """Setup logger with file and console handlers
    
    Args:
        name (str): Logger name
        log_file (str): Log file path
        level (str): Logging level
    
    Returns:
        logging.Logger: Configured logger instance
    """
    config = load_config()
    
    if level is None:
        level = config['logging'].get('level', 'INFO')
    
    if log_file is None:
        log_file = config['logging'].get('log_file', 'logs/automation.log')
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, level.upper()))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Create default logger instance
logger = setup_logger()
