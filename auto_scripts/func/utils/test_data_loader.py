"""Test data loader utility module.

This module provides utilities for loading test data from various sources
including YAML, JSON, and CSV files.
"""

import os
import json
import yaml
import csv
from typing import Dict, List, Any


class TestDataLoader:
    """
    Utility class for loading test data from different file formats.
    """
    
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """
        Load data from a YAML file.
        
        Args:
            file_path (str): Path to the YAML file
        
        Returns:
            dict: Parsed YAML data
        
        Raises:
            FileNotFoundError: If file does not exist
            yaml.YAMLError: If YAML parsing fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        Load data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
        
        Returns:
            dict: Parsed JSON data
        
        Raises:
            FileNotFoundError: If file does not exist
            json.JSONDecodeError: If JSON parsing fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def load_csv(file_path: str, has_header: bool = True) -> List[Dict[str, str]]:
        """
        Load data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            has_header (bool): Whether the CSV has a header row
        
        Returns:
            list: List of dictionaries representing CSV rows
        
        Raises:
            FileNotFoundError: If file does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            if has_header:
                reader = csv.DictReader(f)
                data = list(reader)
            else:
                reader = csv.reader(f)
                data = [{'col_' + str(i): val for i, val in enumerate(row)} 
                       for row in reader]
        
        return data
    
    @staticmethod
    def load_config_data(key_path: str) -> Any:
        """
        Load specific data from config.yaml using dot notation.
        
        Args:
            key_path (str): Dot-separated path to the config value 
                          (e.g., 'test_data.login.valid_user')
        
        Returns:
            Any: The value at the specified path
        
        Raises:
            KeyError: If the path does not exist in config
        """
        config_path = os.path.join(
            os.path.dirname(__file__), '..', 'config', 'config.yaml'
        )
        config = TestDataLoader.load_yaml(config_path)
        
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                raise KeyError(f"Config path not found: {key_path}")
        
        return value
    
    @staticmethod
    def get_test_data_by_scenario(scenario_name: str) -> Dict[str, Any]:
        """
        Get test data for a specific test scenario from config.
        
        Args:
            scenario_name (str): Name of the test scenario
        
        Returns:
            dict: Test data for the scenario
        """
        try:
            return TestDataLoader.load_config_data(f'test_data.{scenario_name}')
        except KeyError:
            return {}


# Convenience functions for quick access
def get_login_credentials(user_type: str = 'valid_user') -> Dict[str, str]:
    """
    Get login credentials for a specific user type.
    
    Args:
        user_type (str): Type of user ('valid_user', 'invalid_user', etc.)
    
    Returns:
        dict: Dictionary with 'username' and 'password' keys
    """
    loader = TestDataLoader()
    return loader.load_config_data(f'test_data.login.{user_type}')


def get_api_config() -> Dict[str, Any]:
    """
    Get API configuration from config file.
    
    Returns:
        dict: API configuration dictionary
    """
    loader = TestDataLoader()
    return loader.load_config_data('api')


def get_ui_config() -> Dict[str, Any]:
    """
    Get UI configuration from config file.
    
    Returns:
        dict: UI configuration dictionary
    """
    loader = TestDataLoader()
    return loader.load_config_data('ui')