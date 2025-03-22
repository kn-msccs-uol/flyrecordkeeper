"""
Flight Record module for FlyRecordKeeper.

This module defines the FlightRecord class for managing flight information.

This project uses a "Structured Dictionaries with OO Benefits" approach where:
1. Records are stored as dictionaries for serialization and storage
2. Classes provide structure, validation, and object-oriented functionality
3. The system maintains the benefits of both approaches
"""
from typing import Dict, Any, List
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
            "date": self.date,#.isoformat(),
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
            date=data["date"],#datetime.fromisoformat(data["date"]),
            start_city=data["start_city"],
            end_city=data["end_city"]
        )
    
    @classmethod
    def validate(cls, data: Dict[str, Any], all_records: List[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Validate flight record data.
        
        Args:
            data: Dictionary containing flight record data
            all_records: List of all records for relationship validation
            
        Returns:
            Dictionary of field validation errors (empty if validation succeeds)
        """
        from utils.validators import validate_required_field, validate_integer, validate_string, validate_date
        
        # Start with base validation
        errors = super().validate(data)
        
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
                if error:
                    errors[field] = error
            elif field == "airline_id":
                error = validate_integer(data[field], "Airline ID", min_value=1)
                if error:
                    errors[field] = error
            elif field == "date":
                error = validate_date(data[field])
                if error:
                    errors[field] = error
            elif field == "start_city":
                error = validate_string(data[field], "Start city", max_length=50)
                if error:
                    errors[field] = error
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
