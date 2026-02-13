"""Logging utility module for the automation framework.

This module provides centralized logging configuration and utilities
for consistent logging across the framework.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class AutomationLogger:
    """
    Centralized logger for the automation framework.
    """
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str, log_level: str = 'INFO') -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name (str): Logger name (typically __name__ of the module)
            log_level (str): Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        
        Returns:
            logging.Logger: Configured logger instance
        """
        if name in AutomationLogger._loggers:
            return AutomationLogger._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Prevent duplicate handlers
        if not logger.handlers:
            # Create logs directory if it doesn't exist
            log_dir = Path(__file__).parent.parent / 'logs'
            log_dir.mkdir(exist_ok=True)
            
            # Create file handler
            log_file = log_dir / f"automation_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        AutomationLogger._loggers[name] = logger
        return logger
    
    @staticmethod
    def log_test_start(test_name: str):
        """
        Log the start of a test.
        
        Args:
            test_name (str): Name of the test
        """
        logger = AutomationLogger.get_logger('test_execution')
        logger.info(f"{'=' * 80}")
        logger.info(f"Starting test: {test_name}")
        logger.info(f"{'=' * 80}")
    
    @staticmethod
    def log_test_end(test_name: str, status: str):
        """
        Log the end of a test.
        
        Args:
            test_name (str): Name of the test
            status (str): Test status ('PASSED', 'FAILED', 'SKIPPED')
        """
        logger = AutomationLogger.get_logger('test_execution')
        logger.info(f"Test {test_name} - Status: {status}")
        logger.info(f"{'=' * 80}\n")
    
    @staticmethod
    def log_step(step_description: str):
        """
        Log a test step.
        
        Args:
            step_description (str): Description of the step
        """
        logger = AutomationLogger.get_logger('test_execution')
        logger.info(f"Step: {step_description}")
    
    @staticmethod
    def log_assertion(assertion_description: str, result: bool):
        """
        Log an assertion result.
        
        Args:
            assertion_description (str): Description of the assertion
            result (bool): Assertion result (True/False)
        """
        logger = AutomationLogger.get_logger('test_execution')
        status = "PASSED" if result else "FAILED"
        logger.info(f"Assertion [{status}]: {assertion_description}")


# Convenience function
def get_logger(name: str = __name__) -> logging.Logger:
    """
    Convenience function to get a logger instance.
    
    Args:
        name (str): Logger name
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return AutomationLogger.get_logger(name)