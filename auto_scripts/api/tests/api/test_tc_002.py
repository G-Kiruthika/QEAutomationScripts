"""Test Case: tc_002 - Add Product

This test verifies that an admin user can successfully login,
navigate to the add product page, enter product details, and create a new product.
"""

import pytest
import yaml
from auto_scripts.Pages.login_page import LoginPage
from auto_scripts.Pages.add_product_page import AddProductPage
from auto_scripts.Pages.base_page import BasePage


def test_tc_002_add_product(driver):
    """Test Add Product functionality.
    
    Steps:
    1. Login as admin user with valid credentials
    2. Verify admin login is successful
    3. Navigate to add product page
    4. Verify add product form is displayed
    5. Enter product details and submit
    6. Verify product is created successfully and appears in product list
    """
    # Initialize page objects
    login_page = LoginPage(driver)
    add_product_page = AddProductPage(driver)
    
    # Test data
    admin_username = "admin"
    admin_password = "valid_admin_password"
    product_name = "sample_product"
    price = "100"
    inventory = "50"
    additional_data = "additional_data"
    
    # Step 1: Login as admin
    login_page.login_as_admin(admin_username, admin_password)
    
    # Step 2: Assert admin login successful
    assert login_page.assert_admin_login_successful(), "Admin login failed"
    
    # Step 3: Navigate to add product page
    add_product_page.navigate_to_add_product()
    
    # Step 4: Assert add product form displayed
    assert add_product_page.assert_add_product_form_displayed(), "Add product form not displayed"
    
    # Step 5: Enter product details and submit
    add_product_page.enter_product_details_and_submit(
        product_name=product_name,
        price=price,
        inventory=inventory,
        etc=additional_data
    )
    
    # Step 6: Assert product created successfully
    assert add_product_page.assert_product_created_successfully(), "Product creation failed or product not visible in list"
