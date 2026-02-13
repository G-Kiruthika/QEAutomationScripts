import logging
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_error(error_message, exception=None):
    """Log error messages with optional exception details"""
    logger.error(f"Error: {error_message}")
    if exception:
        logger.error(f"Exception: {str(exception)}")
        logger.error(f"Traceback: {traceback.format_exc()}")


def log_info(message):
    """Log informational messages"""
    logger.info(message)


def log_warning(message):
    """Log warning messages"""
    logger.warning(message)


def handle_test_exception(test_name, exception):
    """Handle test exceptions with proper logging and reporting"""
    error_msg = f"Test '{test_name}' failed with exception"
    log_error(error_msg, exception)
    return {
        'test_name': test_name,
        'status': 'FAILED',
        'error': str(exception),
        'timestamp': datetime.now().isoformat()
    }


def assert_with_logging(condition, success_message, failure_message):
    """Custom assertion with logging"""
    if condition:
        log_info(success_message)
    else:
        log_error(failure_message)
        assert condition, failure_message