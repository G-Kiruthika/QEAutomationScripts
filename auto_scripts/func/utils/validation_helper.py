# utils/validation_helper.py

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if valid email format, False otherwise
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_password_strength(password: str) -> dict:
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
    
    Returns:
        dict: Dictionary with validation results
    """
    result = {
        'is_valid': True,
        'errors': []
    }
    
    if len(password) < 8:
        result['is_valid'] = False
        result['errors'].append('Password must be at least 8 characters long')
    
    if not re.search(r'[A-Z]', password):
        result['is_valid'] = False
        result['errors'].append('Password must contain at least one uppercase letter')
    
    if not re.search(r'[a-z]', password):
        result['is_valid'] = False
        result['errors'].append('Password must contain at least one lowercase letter')
    
    if not re.search(r'[0-9]', password):
        result['is_valid'] = False
        result['errors'].append('Password must contain at least one digit')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        result['is_valid'] = False
        result['errors'].append('Password must contain at least one special character')
    
    return result


def validate_required_field(value: Optional[str], field_name: str) -> dict:
    """
    Validate that a required field is not empty
    
    Args:
        value (str): Field value to validate
        field_name (str): Name of the field
    
    Returns:
        dict: Dictionary with validation results
    """
    result = {
        'is_valid': True,
        'error': None
    }
    
    if not value or value.strip() == '':
        result['is_valid'] = False
        result['error'] = f'{field_name} is required'
    
    return result


def validate_lockout_message(message: str, expected_keywords: list) -> bool:
    """
    Validate that lockout message contains expected keywords
    
    Args:
        message (str): Actual lockout message
        expected_keywords (list): List of expected keywords
    
    Returns:
        bool: True if all keywords are present, False otherwise
    """
    message_lower = message.lower()
    return all(keyword.lower() in message_lower for keyword in expected_keywords)
