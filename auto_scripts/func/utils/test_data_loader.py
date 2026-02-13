# utils/test_data_loader.py

import yaml
import json
import os


def load_yaml_data(file_path):
    """Load test data from YAML file
    
    Args:
        file_path (str): Path to YAML file
    
    Returns:
        dict: Parsed YAML data
    """
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def load_json_data(file_path):
    """Load test data from JSON file
    
    Args:
        file_path (str): Path to JSON file
    
    Returns:
        dict: Parsed JSON data
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def get_test_data_from_config(key_path):
    """Get test data from config.yaml using dot notation
    
    Args:
        key_path (str): Dot-separated path to data (e.g., 'test_data.valid_user.username')
    
    Returns:
        Any: Value from config
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    keys = key_path.split('.')
    value = config
    for key in keys:
        value = value.get(key)
        if value is None:
            return None
    
    return value
