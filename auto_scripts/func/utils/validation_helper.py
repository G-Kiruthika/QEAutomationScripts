# utils/validation_helper.py

import re

def is_valid_email(email):
    """Validate email format using regex
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if email is valid, False otherwise
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def is_valid_password(password, min_length=8):
    """Validate password strength
    
    Args:
        password (str): Password to validate
        min_length (int): Minimum password length (default: 8)
    
    Returns:
        bool: True if password meets criteria, False otherwise
    """
    if len(password) < min_length:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    return has_upper and has_lower and has_digit and has_special

def is_valid_username(username, min_length=3, max_length=20):
    """Validate username format
    
    Args:
        username (str): Username to validate
        min_length (int): Minimum username length (default: 3)
        max_length (int): Maximum username length (default: 20)
    
    Returns:
        bool: True if username is valid, False otherwise
    """
    if not username or len(username) < min_length or len(username) > max_length:
        return False
    
    # Username should contain only alphanumeric characters and underscores
    username_pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(username_pattern, username) is not None

def passwords_match(password, confirm_password):
    """Check if password and confirm password match
    
    Args:
        password (str): Original password
        confirm_password (str): Confirmation password
    
    Returns:
        bool: True if passwords match, False otherwise
    """
    return password == confirm_password