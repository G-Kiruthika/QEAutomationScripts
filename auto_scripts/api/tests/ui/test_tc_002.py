# Test Case: tc_002 - Add Product
# Feature: Add Product
# Pages Used: LoginPage, AddProductPage

import pytest
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.AddProductPage import AddProductPage
from auto_scripts.core.driver_factory import get_driver
import yaml


def test_tc_002_add_product():
    """
    Test Case: tc_002
    Feature: Add Product
    Flow:
      1. Login as admin
      2. Navigate to add product page
      3. Enter product details and submit
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
        
        # Step 2: Navigate to add product
        add_product_page = AddProductPage(driver)
        add_product_page.navigate_to_add_product()
        assert add_product_page.assert_add_product_form_displayed(), "Add product form not displayed"
        
        # Step 3: Enter product details and submit
        add_product_page.enter_product_details_and_submit(
            name="sample_product",
            price="100",
            description="additional_data"
        )
        assert add_product_page.assert_product_created_successfully(), "Product creation failed"
        
    finally:
        driver.quit()
