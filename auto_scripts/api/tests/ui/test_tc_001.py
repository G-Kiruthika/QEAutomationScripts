# Test Case: tc_001 - Product Catalog Listing
# Feature: Product Catalog Listing
# Pages Used: LoginPage, ProductCatalogPage

import pytest
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ProductCatalogPage import ProductCatalogPage
from auto_scripts.core.driver_factory import get_driver
import yaml


def test_tc_001_product_catalog_listing():
    """
    Test Case: tc_001
    Feature: Product Catalog Listing
    Flow:
      1. Login as admin
      2. Navigate to product catalog
      3. View all products and verify listing
    """
    # Load configuration
    with open('auto_scripts/api/config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    # Initialize driver
    driver = get_driver()
    
    try:
        # Step 1: Login as admin
        login_page = LoginPage(driver)
        login_page.login_as_admin(username="admin", password="valid_admin_password")
        assert login_page.assert_admin_login_successful(), "Admin login failed"
        
        # Step 2: Navigate to catalog
        catalog_page = ProductCatalogPage(driver)
        catalog_page.navigate_to_catalog()
        assert catalog_page.assert_product_catalog_displayed(), "Product catalog page not displayed"
        
        # Step 3: View all products
        catalog_page.view_all_products()
        assert catalog_page.assert_all_products_listed(), "Products not listed correctly"
        
    finally:
        driver.quit()
