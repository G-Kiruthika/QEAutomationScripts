# Test Data Loader for Dynamic Test Data Management
import yaml
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TestDataLoader:
    """Load and manage test data from various sources."""
    
    @staticmethod
    def load_yaml_config(config_path='config/config.yaml'):
        """Load configuration from YAML file."""
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config
            else:
                logger.warning(f"Config file not found: {config_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return {}
    
    @staticmethod
    def load_json_data(json_path):
        """Load test data from JSON file."""
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Test data loaded from {json_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON data: {str(e)}")
            return {}
    
    @staticmethod
    def get_test_user(user_type='valid_user'):
        """Get test user credentials from config."""
        config = TestDataLoader.load_yaml_config()
        try:
            user_data = config.get('ecommerce', {}).get('test_users', {}).get(user_type, {})
            return user_data
        except Exception as e:
            logger.error(f"Error retrieving test user {user_type}: {str(e)}")
            return {}
    
    @staticmethod
    def get_login_url(url_type='primary'):
        """Get login URL from config."""
        config = TestDataLoader.load_yaml_config()
        try:
            url = config.get('ecommerce', {}).get('login_urls', {}).get(url_type, '')
            return url
        except Exception as e:
            logger.error(f"Error retrieving login URL {url_type}: {str(e)}")
            return ''
