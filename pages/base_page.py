from core.selenium_wrapper import SeleniumWrapper
import yaml
import os

class BasePage(SeleniumWrapper):
    """Base page class that all page objects inherit from"""
    
    def __init__(self, driver):
        super().__init__(driver)
        
        # Load base URL from configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        self.base_url = config.get('environment', {}).get('base_url', 'https://example.com')
    
    def navigate_to_url(self, url):
        """Navigate to specific URL"""
        full_url = self.base_url + url if not url.startswith('http') else url
        self.driver.get(full_url)
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url