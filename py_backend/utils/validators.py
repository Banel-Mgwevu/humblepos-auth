# ==================== utils/validators.py ====================
"""
Validation utilities module.
Contains validation functions for user input.
"""

import re


def validate_email(email):
    """
    Validate email address format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def validate_password(password, min_length=8):
    """
    Validate password meets minimum requirements.
    
    Args:
        password (str): Password to validate
        min_length (int): Minimum password length
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    
    return True, None


def validate_name(name, field_name="Name"):
    """
    Validate name field.
    
    Args:
        name (str): Name to validate
        field_name (str): Field name for error messages
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, f"{field_name} is required"
    
    name = name.strip()
    
    if len(name) < 1:
        return False, f"{field_name} cannot be empty"
    
    if len(name) > 100:
        return False, f"{field_name} cannot exceed 100 characters"
    
    return True, None

