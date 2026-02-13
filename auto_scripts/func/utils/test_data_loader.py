import yaml
import json
import os


def load_yaml_config(file_path):
    """
    Load YAML configuration file
    
    Args:
        file_path (str): Path to YAML file
    
    Returns:
        dict: Parsed YAML content
    """
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def load_json_data(file_path):
    """
    Load JSON data file
    
    Args:
        file_path (str): Path to JSON file
    
    Returns:
        dict: Parsed JSON content
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def get_test_data(data_key, config_path=None):
    """
    Get test data from config.yaml
    
    Args:
        data_key (str): Key path to test data (e.g., 'test_data.valid_credentials')
        config_path (str): Optional custom config path
    
    Returns:
        Any: Test data value
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    config = load_yaml_config(config_path)
    
    # Navigate nested keys
    keys = data_key.split('.')
    value = config
    for key in keys:
        value = value.get(key, {})
    
    return value


def get_credentials(credential_type='valid_credentials'):
    """
    Get login credentials from config
    
    Args:
        credential_type (str): Type of credentials ('valid_credentials', 'invalid_credentials')
    
    Returns:
        dict: Username and password
    """
    return get_test_data(f'test_data.{credential_type}')
