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
    """Log error with traceback if exception is provided"""
    logger.error(error_message)
    if exception:
        logger.error(f"Exception: {str(exception)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

def log_info(message):
    """Log informational message"""
    logger.info(message)

def log_warning(message):
    """Log warning message"""
    logger.warning(message)

def handle_test_exception(test_name, exception):
    """Handle test exception with logging and reporting"""
    error_msg = f"Test '{test_name}' failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    log_error(error_msg, exception)
    return error_msg

def safe_execute(func, *args, **kwargs):
    """Safely execute a function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_error(f"Error executing {func.__name__}", e)
        raise
