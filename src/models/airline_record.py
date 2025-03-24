"""
Airline Record module for FlyRecordKeeper.

This module defines the AirlineRecord class for managing airline information.

This project uses a "Structured Dictionaries with OO Benefits" approach where:
1. Records are stored as dictionaries for serialization and storage
2. Classes provide structure, validation, and object-oriented functionality
3. The system maintains the benefits of both approaches
"""
from typing import Dict, Any

from models.base_record import BaseRecord
from utils.validators import validate_required_field, validate_string


class AirlineRecord(BaseRecord):
    """
    Class for managing airline records in the system.
    
    Extends BaseRecord with airline-specific attributes.
    """
    
    def __init__(self, record_id: int, company_name: str):
        """
        Initialize a new AirlineRecord instance.
        
        Args:
            record_id: Unique identifier for the airline
            company_name: Name of the airline company
        """
        super().__init__(record_id, "airline")
        self.company_name = company_name
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the airline record to a dictionary for storage.
        
        Returns:
            Dictionary representation of the airline record
        """
        airline_dict = super().to_dict()
        airline_dict.update({
            "company_name": self.company_name
        })
        return airline_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AirlineRecord':
        """
        Create an airline record from a dictionary.
        
        Args:
            data: Dictionary containing airline record data
            
        Returns:
            A new AirlineRecord instance
        """
        return cls(
            record_id=data["id"],
            company_name=data["company_name"]
        )
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate airline record data.
        
        Args:
            data: Dictionary containing airline record data
            
        Returns:
            Dictionary of field validation errors (empty if validation succeeds)
        """    
        # Start with base validation
        errors = super().validate(data)
        
        # Company name is required
        error = validate_required_field(data, "company_name")
        if error:
            errors["company_name"] = error
        elif "company_name" in data:
            error = validate_string(data["company_name"], "Company name", max_length=100)
            if error:
                errors["company_name"] = error
        
        return errors
