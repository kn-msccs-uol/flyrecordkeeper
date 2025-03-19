"""
Base Record class module for FlyRecordKeeper.

This module defines the BaseRecord class that serves as the parent class
for all record types in the system.

This project uses a "Structured Dictionaries with OO Benefits" approach where:
1. Records are stored as dictionaries for serialization and storage
2. Classes provide structure, validation, and object-oriented functionality
3. The system maintains the benefits of both approaches
"""
from typing import Dict, Any


class BaseRecord:
    """
    Base class for all record types in the system.
    
    Provides common attributes and methods for all record types.
    """
    
    def __init__(self, record_id: int, record_type: str):
        """
        Initialize a new BaseRecord instance.
        
        Args:
            record_id: Unique identifier for the record
            record_type: Type of record (e.g., 'client', 'airline', 'flight')
        """
        self.id = record_id
        self.type = record_type
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the record to a dictionary for storage.
        
        Returns:
            Dictionary representation of the record
        """
        return {
            "id": self.id,
            "type": self.type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseRecord':
        """
        Create a record from a dictionary.
        
        Args:
            data: Dictionary containing record data
            
        Returns:
            A new BaseRecord instance
        """
        return cls(record_id=data["id"], record_type=data["type"])
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate basic record data.
        
        Args:
            data: Dictionary containing record data
            
        Returns:
            Dictionary of field validation errors (empty if validation succeeds)
        """
        errors = {}
        
        # Validate ID if present
        if "id" in data and not isinstance(data["id"], int):
            errors["id"] = "ID must be an integer"
        
        # Validate type if present
        if "type" in data and not isinstance(data["type"], str):
            errors["type"] = "Type must be a string"
            
        return errors
