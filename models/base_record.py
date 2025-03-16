"""
Base Record class module for FlyRecordKeeper.

This module defines the BaseRecord class that serves as the parent class
for all record types in the system.
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
