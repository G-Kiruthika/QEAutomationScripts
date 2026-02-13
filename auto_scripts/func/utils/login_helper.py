# Login Helper Utility for Common Login Operations
import logging
from utils.session_manager import SessionManager

logger = logging.getLogger(__name__)

class LoginHelper:
    """Helper class for common login operations and validations."""
    
    @staticmethod
    def perform_login(login_page, email, password):
        """Perform complete login flow with error handling."""
        try:
            login_page.enter_email(email)
            login_page.enter_password_xpath(password)
            login_page.click_login_xpath()
            logger.info(f"Login attempted for user: {email}")
            return True
        except Exception as e:
            logger.error(f"Login failed for user {email}: {str(e)}")
            return False
    
    @staticmethod
    def validate_successful_login(login_page, driver):
        """Validate all aspects of successful login."""
        validations = {
            'dashboard_visible': login_page.verify_login_success(),
            'session_created': login_page.verify_user_session(),
            'session_token_exists': SessionManager.validate_session_token(driver)
        }
        
        all_valid = all(validations.values())
        logger.info(f"Login validation results: {validations}")
        return all_valid
    
    @staticmethod
    def validate_failed_login(login_page):
        """Validate login failure indicators."""
        validations = {
            'error_message_visible': login_page.verify_login_failure(),
            'remains_on_login_page': login_page.verify_remain_on_login()
        }
        
        all_valid = all(validations.values())
        logger.info(f"Login failure validation results: {validations}")
        return all_valid
