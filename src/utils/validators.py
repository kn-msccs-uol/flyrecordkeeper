"""
Validators module for FlyRecordKeeper.

This module provides validation functions for record fields.
"""
import re
from datetime import datetime
from typing import Any, Optional, Dict


def validate_required_field(data: Dict[str, Any], field_name: str) -> Optional[str]:
    """
    Validate that a required field exists and is not empty.
    
    Args:
        data: Dictionary containing record data
        field_name: Name of the required field
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if field_name not in data:
        return f"{field_name} is required"
    
    if isinstance(data[field_name], str) and not data[field_name].strip():
        return f"{field_name} cannot be empty"
        
    return None


def validate_string(value: Any, field_name: str, min_length: int = 1, 
                   max_length: int = 100) -> Optional[str]:
    """
    Validate a string field.
    
    Args:
        value: Value to validate
        field_name: Name of the field being validated
        min_length: Minimum acceptable length
        max_length: Maximum acceptable length
    
    Returns:
        Error message if validation fails, None otherwise
    """
    if not isinstance(value, str):
        return f"{field_name} must be a string"
    
    if len(value) < min_length:
        return f"{field_name} must be at least {min_length} characters"
    
    if len(value) > max_length:
        return f"{field_name} must be at most {max_length} characters"
    
    return None


def validate_integer(value: Any, field_name: str, min_value: Optional[int] = None, 
                    max_value: Optional[int] = None) -> Optional[str]:
    """
    Validate an integer field.
    
    Args:
        value: Value to validate
        field_name: Name of the field being validated
        min_value: Minimum acceptable value (optional)
        max_value: Maximum acceptable value (optional)
    
    Returns:
        Error message if validation fails, None otherwise
    """
    if not isinstance(value, int):
        return f"{field_name} must be an integer"
    
    if min_value is not None and value < min_value:
        return f"{field_name} must be at least {min_value}"
    
    if max_value is not None and value > max_value:
        return f"{field_name} must be at most {max_value}"
    
    return None


def validate_phone_number(value: str, field_name: str = "Phone number") -> Optional[str]:
    """
    Validate a phone number.
    
    Args:
        value: Value to validate
        field_name: Name of the field being validated
    
    Returns:
        Error message if validation fails, None otherwise
    """
    # First check it's a string
    string_validation = validate_string(value, field_name)
    if string_validation:
        return string_validation
    
    # Simple pattern: allow digits, spaces, plus, hyphens, parentheses
    pattern = r'^[0-9\s\+\-\(\)]+$'
    if not re.match(pattern, value):
        return f"{field_name} contains invalid characters"
    
    # Ensure there are at least some digits
    if not any(c.isdigit() for c in value):
        return f"{field_name} must contain some digits"
    
    return None


def validate_date(value: Any, field_name: str = "Date") -> Optional[str]:
    """
    Validate a date value.
    
    Args:
        value: Value to validate (should be a datetime object)
        field_name: Name of the field being validated
    
    Returns:
        Error message if validation fails, None otherwise
    """
    if not isinstance(value, datetime):
        return f"{field_name} must be a datetime object"
    
    return None


def get_validation_errors_summary(errors: Dict[str, str]) -> str:
    """
    Create a human-readable summary of validation errors.
    
    Args:
        errors: Dictionary of field validation errors
        
    Returns:
        Formatted error message string, or empty string if no errors
    """
    if not errors:
        return ""
        
    return "; ".join(f"{key}: {value}" for key, value in errors.items())
