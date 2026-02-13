# Session Management Utility for Login Flow
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Utility class to manage user session validation and tracking."""
    
    @staticmethod
    def validate_session_token(driver):
        """Validate if session token exists in cookies or local storage."""
        try:
            cookies = driver.get_cookies()
            session_cookie = [cookie for cookie in cookies if 'session' in cookie.get('name', '').lower()]
            if session_cookie:
                logger.info(f"Session token found: {session_cookie[0]['name']}")
                return True
            logger.warning("No session token found in cookies")
            return False
        except Exception as e:
            logger.error(f"Error validating session token: {str(e)}")
            return False
    
    @staticmethod
    def get_session_username(driver):
        """Extract username from session display element."""
        try:
            username_element = driver.find_element("xpath", "//header//span[@class='username']")
            username = username_element.text
            logger.info(f"Session username: {username}")
            return username
        except Exception as e:
            logger.error(f"Error retrieving session username: {str(e)}")
            return None
    
    @staticmethod
    def clear_session(driver):
        """Clear all session cookies and local storage."""
        try:
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            logger.info("Session cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing session: {str(e)}")
            return False
