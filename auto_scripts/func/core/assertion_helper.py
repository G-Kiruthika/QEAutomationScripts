# Assertion Helper for Enhanced Test Validations
import logging

logger = logging.getLogger(__name__)

class AssertionHelper:
    """Enhanced assertion methods with detailed logging."""
    
    @staticmethod
    def assert_element_visible(element_visible, element_name):
        """Assert element is visible with custom message."""
        try:
            assert element_visible, f"{element_name} is not visible"
            logger.info(f"Assertion passed: {element_name} is visible")
            return True
        except AssertionError as e:
            logger.error(f"Assertion failed: {str(e)}")
            raise
    
    @staticmethod
    def assert_text_equals(actual_text, expected_text, field_name):
        """Assert text equality with custom message."""
        try:
            assert actual_text == expected_text, f"{field_name} text mismatch. Expected: '{expected_text}', Actual: '{actual_text}'"
            logger.info(f"Assertion passed: {field_name} text matches '{expected_text}'")
            return True
        except AssertionError as e:
            logger.error(f"Assertion failed: {str(e)}")
            raise
    
    @staticmethod
    def assert_url_contains(driver, url_fragment):
        """Assert current URL contains specific fragment."""
        try:
            current_url = driver.current_url
            assert url_fragment in current_url, f"URL does not contain '{url_fragment}'. Current URL: {current_url}"
            logger.info(f"Assertion passed: URL contains '{url_fragment}'")
            return True
        except AssertionError as e:
            logger.error(f"Assertion failed: {str(e)}")
            raise
    
    @staticmethod
    def soft_assert(condition, message):
        """Soft assertion that logs failure but doesn't stop execution."""
        if not condition:
            logger.warning(f"Soft assertion failed: {message}")
            return False
        logger.info(f"Soft assertion passed: {message}")
        return True
