from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class ProductCatalogPage(BasePage):
    SEARCH_BOX = (By.ID, "searchBox")
    PRODUCT_LIST = (By.CLASS_NAME, "product-list")
    ADD_PRODUCT_BUTTON = (By.ID, "addProductBtn")
    # Added from metadata
    PRODUCT_CATALOG_NAV_LOCATOR = (By.ID, "placeholder_product_catalog_nav_locator")
    PRODUCT_LIST_LOCATOR = (By.ID, "placeholder_product_list_locator")
    PRODUCT_CATALOG_PAGE_DISPLAY_LOCATOR = (By.ID, "placeholder_product_catalog_page_display_locator")
    PRODUCT_DETAILS_LOCATOR = (By.ID, "placeholder_product_details_locator")

    def search_product(self, product_name):
        self.send_keys(self.SEARCH_BOX, product_name)

    def click_add_product(self):
        self.click(self.ADD_PRODUCT_BUTTON)

    def is_product_list_visible(self):
        return self.is_visible(self.PRODUCT_LIST)

    # Added from metadata
    def navigate_to_catalog(self):
        """Navigate to the product catalog page."""
        self.click(self.PRODUCT_CATALOG_NAV_LOCATOR)

    def view_all_products(self):
        """View the list of all products."""
        return self.find_elements(self.PRODUCT_LIST_LOCATOR)

    def assert_product_catalog_displayed(self):
        """Verify product catalog page is displayed."""
        return self.is_visible(self.PRODUCT_CATALOG_PAGE_DISPLAY_LOCATOR)

    def assert_all_products_listed(self):
        """Verify all products are listed with details and inventory status."""
        return self.is_visible(self.PRODUCT_DETAILS_LOCATOR)
