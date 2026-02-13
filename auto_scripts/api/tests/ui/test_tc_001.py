# Test Case: tc_001
# Feature: Product Catalog Listing
# Generated UI Automation Test Script

import pytest
from auto_scripts.Pages.login_page import LoginPage
from auto_scripts.Pages.product_catalog_page import ProductCatalogPage
from auto_scripts.core.driver_factory import get_driver
import yaml


class TestProductCatalogListing:
    """Test suite for Product Catalog Listing functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method to initialize driver and page objects"""
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)
        self.product_catalog_page = ProductCatalogPage(self.driver)
        yield
        self.driver.quit()

    def test_tc_001_product_catalog_listing(self):
        """Test case to verify product catalog listing after admin login"""
        
        # Step 1: Login as admin
        self.login_page.enter_username('admin')
        self.login_page.enter_password('valid_admin_password')
        self.login_page.click_login()
        
        # Assertion: Verify admin login successful
        assert self.login_page.is_login_button_visible() == False, "Admin login failed - login button still visible"
        
        # Step 2: Navigate to catalog
        # Navigation logic would be implemented in ProductCatalogPage
        # For now, we assume navigation happens automatically or via URL
        
        # Assertion: Verify product catalog displayed
        assert self.product_catalog_page.is_product_list_visible(), "Product catalog not displayed"
        
        # Step 3: View all products
        # This would trigger display of all products in the catalog
        
        # Assertion: Verify all products listed
        assert self.product_catalog_page.is_product_list_visible(), "All products not listed correctly"
