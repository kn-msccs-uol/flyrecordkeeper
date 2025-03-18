"""
Validators module for FlyRecordKeeper.

This module provides validation functions for record fields.
"""
import re
from datetime import datetime
from typing import Any, Optional, Dict, List


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
    required_fields = ["name", "address_line1", "address_line2", "address_line3", "city", "state",
                       "zip_code", "country", "phone_number"]
    for field in required_fields:
        error = validate_required_field(data, field)
        if error:
            errors[field] = error
            continue

        # Field-specific validation
        if field == "name":
            error = validate_string(data[field], "Name", max_length=100)
        elif field == "address_line1":
            error = validate_string(data[field], "Address line 1", max_length=100)
        elif field == "address_line2":
            error = validate_string(data[field], "Address line 2", max_length=100)
        elif field == "address_line3":
            error = validate_string(data[field], "Address line 3", max_length=100)
        elif field == "city":
            error = validate_string(data[field], "City", max_length=50)
        elif field == "state":
            error = validate_string(data[field], "State", max_length=50)
        elif field == "zip_code":
            error = validate_string(data[field], "Zip code", max_length=20)
        elif field == "country":
            error = validate_string(data[field], "Country", max_length=100)
        elif field == "phone_number":
            error = validate_phone_number(data[field])

        if error:
            errors[field] = error

    # Optional fields
    #optional_fields = {
    #    "address_line2": ("Address line 2", 0, 100),
    #    "address_line3": ("Address line 3", 0, 100),
    #    }
    
    #for field, (display_name, min_len, max_len) in optional_fields.items():
    #    if field in data and data[field]:
    #        error = validate_string(data[field], display_name, min_len, max_len)
    #        if error:
    #            errors[field] = error
    
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
    
    # Company name is required
    error = validate_required_field(data, "company_name")
    if error:
        errors["company_name"] = error
    elif "company_name" in data:
        error = validate_string(data["company_name"], "Company name", max_length=100)
        if error:
            errors["company_name"] = error

    return errors


def validate_flight_record(data: Dict[str, Any], all_records: List[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Validate a flight record including relationship validation.
    
    Args:
        data: Dictionary containing flight record data
        all_records: List of all records for relationship validation
    
    Returns:
        Dictionary of field validation errors (empty if validation succeeds)
    """
    errors = {}
    
    # Required fields
    required_fields = ["client_id", "airline_id", "date", "start_city", "end_city"]
    for field in required_fields:
        error = validate_required_field(data, field)
        if error:
            errors[field] = error
            continue

        # Field-specific validation
        if field == "client_id":
            error = validate_integer(data[field], "Client ID", min_value=1)
        elif field == "airline_id":
            error = validate_integer(data[field], "Airline ID", min_value=1)
        elif field == "date":
            error = validate_date(data[field])
        elif field == "start_city":
            error = validate_string(data[field], "Start city", max_length=50)
        elif field == "end_city":
            error = validate_string(data[field], "End city", max_length=50)
            
        if error:
            errors[field] = error

    # Relationship validation if records are provided
    if all_records and "client_id" in data and "airline_id" in data:
        # Check client exists
        if not any(r.get("id") == data["client_id"] and r.get("type") == "client" 
                for r in all_records):
            errors["client_id"] = f"Client with ID {data['client_id']} does not exist"
        
        # Check airline exists
        if not any(r.get("id") == data["airline_id"] and r.get("type") == "airline" 
                for r in all_records):
            errors["airline_id"] = f"Airline with ID {data['airline_id']} does not exist"
    
    return errors
