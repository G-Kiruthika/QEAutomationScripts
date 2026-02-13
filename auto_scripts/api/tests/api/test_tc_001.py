"""Test Case: tc_001 - Product Catalog Listing

This test verifies that an admin user can successfully login,
navigate to the product catalog, and view all products with their details.
"""

import pytest
import yaml
from auto_scripts.Pages.login_page import LoginPage
from auto_scripts.Pages.product_catalog_page import ProductCatalogPage
from auto_scripts.Pages.base_page import BasePage


def test_tc_001_product_catalog_listing(driver):
    """Test Product Catalog Listing functionality.
    
    Steps:
    1. Login as admin user with valid credentials
    2. Verify admin login is successful
    3. Navigate to product catalog
    4. Verify product catalog page is displayed
    5. View all products
    6. Verify all products are listed with details and inventory status
    """
    # Initialize page objects
    login_page = LoginPage(driver)
    product_catalog_page = ProductCatalogPage(driver)
    
    # Test data
    admin_username = "admin"
    admin_password = "valid_admin_password"
    
    # Step 1: Login as admin
    login_page.login_as_admin(admin_username, admin_password)
    
    # Step 2: Assert admin login successful
    assert login_page.assert_admin_login_successful(), "Admin login failed"
    
    # Step 3: Navigate to product catalog
    product_catalog_page.navigate_to_catalog()
    
    # Step 4: Assert product catalog displayed
    assert product_catalog_page.assert_product_catalog_displayed(), "Product catalog page not displayed"
    
    # Step 5: View all products
    products = product_catalog_page.view_all_products()
    
    # Step 6: Assert all products listed
    assert product_catalog_page.assert_all_products_listed(), "Not all products are listed with details"
    assert len(products) > 0, "No products found in catalog"
