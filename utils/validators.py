"""
Validators module for FlyRecordKeeper.

This module provides validation functions for record fields.
"""
import re
from datetime import datetime
from typing import Any, Optional, Dict


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


def validate_client_record(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate a client record.
    
    Args:
        data: Dictionary containing client record data
    
    Returns:
        Dictionary of field validation errors (empty if validation succeeds)
    """
    errors = {}
    
    # Required fields
    if "name" in data:
        error = validate_string(data["name"], "Name", max_length=100)
        if error:
            errors["name"] = error
    else:
        errors["name"] = "Name is required"
    
    if "address_line1" in data:
        error = validate_string(data["address_line1"], "Address line 1", max_length=100)
        if error:
            errors["address_line1"] = error
    else:
        errors["address_line1"] = "Address line 1 is required"

    if "address_line2" in data: # {To make it optional} and data["address_line2"]:
        error = validate_string(data["address_line2"], "Address line 2", min_length=0, max_length=100)
        if error:
            errors["address_line2"] = error
    else:
        errors["address_line2"] = "Address line 2 is required"
    
    if "address_line3" in data: # {To make it optional} and data["address_line3"]:
        error = validate_string(data["address_line3"], "Address line 3", min_length=0, max_length=100)
        if error:
            errors["address_line3"] = error
    else:
        errors["address_line3"] = "Address line 3 is required"
    
    if "city" in data:
        error = validate_string(data["city"], "City", max_length=50)
        if error:
            errors["city"] = error
    else:
        errors["city"] = "City is required"

    if "state" in data: # {To make it optional} and data["state"]:
        error = validate_string(data["state"], "State", min_length=0, max_length=50)
        if error:
            errors["state"] = error
    else:
        errors["state"] = "State is required"

    if "zip_code" in data: # {To make it optional} and data["zip_code"]:
        error = validate_string(data["zip_code"], "Zip code", min_length=0, max_length=20)
        if error:
            errors["zip_code"] = error
    else:
        errors["zip_code"] = "Zip Code is required"
    
    if "country" in data:
        error = validate_string(data["country"], "Country", max_length=50)
        if error:
            errors["country"] = error
    else:
        errors["country"] = "Country is required"
    
    if "phone_number" in data:
        error = validate_phone_number(data["phone_number"])
        if error:
            errors["phone_number"] = error
    else:
        errors["phone_number"] = "Phone number is required"
    
    return errors


def validate_airline_record(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate an airline record.
    
    Args:
        data: Dictionary containing airline record data
    
    Returns:
        Dictionary of field validation errors (empty if validation succeeds)
    """
    errors = {}
    
    # Required fields
    if "company_name" in data:
        error = validate_string(data["company_name"], "Company name", max_length=100)
        if error:
            errors["company_name"] = error
    else:
        errors["company_name"] = "Company name is required"
    
    return errors


def validate_flight_record(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate a flight record.
    
    Args:
        data: Dictionary containing flight record data
    
    Returns:
        Dictionary of field validation errors (empty if validation succeeds)
    """
    errors = {}
    
    # Required fields
    if "client_id" in data:
        error = validate_integer(data["client_id"], "Client ID", min_value=1)
        if error:
            errors["client_id"] = error
    else:
        errors["client_id"] = "Client ID is required"
    
    if "airline_id" in data:
        error = validate_integer(data["airline_id"], "Airline ID", min_value=1)
        if error:
            errors["airline_id"] = error
    else:
        errors["airline_id"] = "Airline ID is required"
    
    if "date" in data:
        error = validate_date(data["date"])
        if error:
            errors["date"] = error
    else:
        errors["date"] = "Date is required"
    
    if "start_city" in data:
        error = validate_string(data["start_city"], "Start city", max_length=50)
        if error:
            errors["start_city"] = error
    else:
        errors["start_city"] = "Start city is required"
    
    if "end_city" in data:
        error = validate_string(data["end_city"], "End city", max_length=50)
        if error:
            errors["end_city"] = error
    else:
        errors["end_city"] = "End city is required"
    
    return errors
