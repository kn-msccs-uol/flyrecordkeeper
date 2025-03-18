"""
Flight Record module for FlyRecordKeeper.

This module defines the FlightRecord class for managing flight information.
"""
from typing import Dict, Any
from datetime import datetime
from models.base_record import BaseRecord


class FlightRecord(BaseRecord):
    """
    Class for managing flight records in the system.
    
    Extends BaseRecord with flight-specific attributes.
    """
    
    def __init__(self, record_id: int, client_id: int, airline_id: int, 
                 date: datetime, start_city: str, end_city: str):
        """
        Initialize a new FlightRecord instance.
        
        Args:
            record_id: Unique identifier for the client-flight record
            client_id: ID of the client taking the flight
            airline_id: ID of the airline operating the flight
            date: Date and time of the flight
            start_city: Departure city
            end_city: Destination city
        """
        super().__init__(record_id, "flight")
        self.client_id = client_id
        self.airline_id = airline_id
        self.date = date
        self.start_city = start_city
        self.end_city = end_city
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the flight record to a dictionary for storage.
        
        Returns:
            Dictionary representation of the flight record
        """
        flight_dict = super().to_dict()
        flight_dict.update({
            "client_id": self.client_id,
            "airline_id": self.airline_id,
            "date": self.date.isoformat(),
            "start_city": self.start_city,
            "end_city": self.end_city
        })
        return flight_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FlightRecord':
        """
        Create a flight record from a dictionary.
        
        Args:
            data: Dictionary containing flight record data
            
        Returns:
            A new FlightRecord instance
        """
        return cls(
            record_id=data["id"],
            client_id=data["client_id"],
            airline_id=data["airline_id"],
            date=datetime.fromisoformat(data["date"]),
            start_city=data["start_city"],
            end_city=data["end_city"]
        )
