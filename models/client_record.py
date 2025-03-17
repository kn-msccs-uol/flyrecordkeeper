"""
Client Record module for FlyRecordKeeper.

This module defines the ClientRecord class for managing client information.
"""
from typing import Dict, Any
from base_record import BaseRecord


class ClientRecord(BaseRecord):
    """
    Class for managing client records in the system.
    
    Extends BaseRecord with client-specific attributes.
    """
    
    def __init__(self, record_id: int, name: str, address_line1: str,
                 address_line2: str, address_line3: str, city: str,
                 state: str, zip_code: str, country: str, phone_number: str):
        """
        Initialize a new ClientRecord instance.
        
        Args:
            record_id: Unique identifier for the client
            name: Full name of the client
            address_line1: First line of client's address
            city: Client's city
            country: Client's country
            phone_number: Client's contact number
            address_line2: Second line of client's address (optional)
            address_line3: Third line of client's address (optional)
            state: Client's state or province (optional)
            zip_code: Client's postal code (optional)
        """
        super().__init__(record_id, "client")
        self.name = name
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone_number = phone_number
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the client record to a dictionary for storage.
        
        Returns:
            Dictionary representation of the client record
        """
        client_dict = super().to_dict()
        client_dict.update({
            "name": self.name,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "address_line3": self.address_line3,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "phone_number": self.phone_number
        })
        return client_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClientRecord':
        """
        Create a client record from a dictionary.
        
        Args:
            data: Dictionary containing client record data
            
        Returns:
            A new ClientRecord instance
        """
        return cls(
            record_id=data["id"],
            name=data["name"],
            address_line1=data["address_line1"],
            address_line2=data["address_line2"],
            address_line3=data["address_line3"],
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
            country=data["country"],
            phone_number=data["phone_number"]
        )
