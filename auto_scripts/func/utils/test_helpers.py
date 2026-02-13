"""Test Helper Utilities

Provides utility functions for test execution, data handling,
and common test operations.
"""

import logging
import yaml
import os
from typing import Any, Dict


logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {config_path}")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {str(e)}")
        raise


def get_test_data(test_name: str, config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """Retrieve test data for a specific test.
    
    Args:
        test_name (str): Name of the test
        config_path (str): Path to the configuration file
        
    Returns:
        Dict[str, Any]: Test data dictionary
    """
    config = load_config(config_path)
    test_data = config.get('test_data', {}).get(test_name, {})
    logger.info(f"Test data retrieved for: {test_name}")
    return test_data


def assert_with_logging(condition: bool, message: str):
    """Assert with logging support.
    
    Args:
        condition (bool): Condition to assert
        message (str): Assertion message
        
    Raises:
        AssertionError: If condition is False
    """
    if not condition:
        logger.error(f"Assertion failed: {message}")
        assert condition, message
    else:
        logger.info(f"Assertion passed: {message}")


def create_directory_if_not_exists(directory_path: str):
    """Create directory if it doesn't exist.
    
    Args:
        directory_path (str): Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Directory created: {directory_path}")


def validate_email(email: str) -> bool:
    """Validate email format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(pattern, email))
    logger.debug(f"Email validation for {email}: {is_valid}")
    return is_valid
