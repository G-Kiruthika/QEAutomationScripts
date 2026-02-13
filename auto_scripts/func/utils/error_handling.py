import logging
import traceback
from datetime import datetime
import os

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"automation_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def handle_exception(exception, context=""):
    """Handle exceptions with logging and reporting
    
    Args:
        exception: The exception object
        context: Additional context information about where the exception occurred
    """
    error_message = f"Exception occurred in {context}: {str(exception)}"
    logger.error(error_message)
    logger.error(f"Traceback: {traceback.format_exc()}")
    return error_message


def log_test_step(step_name, status="STARTED", details=""):
    """Log test step execution
    
    Args:
        step_name: Name of the test step
        status: Status of the step (STARTED, PASSED, FAILED)
        details: Additional details about the step
    """
    log_message = f"Test Step: {step_name} - Status: {status}"
    if details:
        log_message += f" - Details: {details}"
    
    if status == "FAILED":
        logger.error(log_message)
    else:
        logger.info(log_message)


def capture_screenshot(driver, test_name):
    """Capture screenshot on test failure
    
    Args:
        driver: WebDriver instance
        test_name: Name of the test
    
    Returns:
        str: Path to the saved screenshot
    """
    screenshot_dir = "reports/screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
    
    try:
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {str(e)}")
        return None


def assert_with_logging(condition, success_message, failure_message):
    """Assert with logging support
    
    Args:
        condition: Boolean condition to assert
        success_message: Message to log on success
        failure_message: Message to log on failure
    """
    if condition:
        logger.info(success_message)
    else:
        logger.error(failure_message)
        raise AssertionError(failure_message)