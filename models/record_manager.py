"""
Record Manager module for FlyRecordKeeper.

This module provides functionality for creating, reading, updating,
and deleting (CRUD) records in the system.
"""
import os
from typing import List, Dict, Any, Union, Optional
from datetime import datetime

# Import the record classes
from base_record import BaseRecord
from client_record import ClientRecord
from airline_record import AirlineRecord
from flight_record import FlightRecord

# Import the file handler
from utils.file_handler import load_records, save_records, dict_to_record

# Import the validator
from utils.validators import (validate_client_record, validate_airline_record, validate_flight_record)


class RecordManager:
    """
    Class for managing records in the system.
    
    Handles record creation, retrieval, updating, and deletion (CRUD).
    """
    
    def __init__(self, filename: str = "data/records.json"):
        """
        Initialize a new RecordManager instance.
        
        Args:
            filename: Path to the JSON file where records are stored
        """
        self.filename = filename
        self.records = []
        self.load_from_file()
    
    def load_from_file(self) -> bool:
        """
        Load records from the JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.records = load_records(self.filename)
            return True
        except Exception as e:
            print(f"Error loading records: {e}")
            return False
    
    def save_to_file(self) -> bool:
        """
        Save records to the JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        return save_records(self.records, self.filename)
    
    def get_next_id(self) -> int:
        """
        Generate the next available record ID.
        
        Returns:
            Next available ID
        """
        if not self.records:
            return 1
        
        # Find the maximum ID currently in use
        max_id = 0
        for record in self.records:
            if "id" in record and record["id"] > max_id:
                max_id = record["id"]
        
        return max_id + 1
    
    def create_client(self, name: str, address_line1: str, address_line2: str, 
                     address_line3: str, city: str, state: str, zip_code: str,
                     country: str, phone_number: str) -> Dict[str, Any]:
        """
        Create a new client record.
        
        Args:
            name: Client's name
            address_line1: First line of client's address
            address_line2: Second line of client's address
            address_line3: Third line of client's address
            city: Client's city
            state: Client's state
            zip_code: Client's postal code
            country: Client's country
            phone_number: Client's phone number
            
        Returns:
            Dictionary containing the created client record
        """
        # Generate a new ID
        record_id = self.get_next_id()
        
        # Create a new client record
        client = ClientRecord(
            record_id=record_id,
            name=name,
            address_line1=address_line1,
            address_line2=address_line2,
            address_line3=address_line3,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            phone_number=phone_number
        )
        
        # Convert to dictionary and add to records
        client_dict = client.to_dict()
        self.records.append(client_dict)
        
        # Save to file
        self.save_to_file()
        
        return client_dict
    
    def create_airline(self, company_name: str) -> Dict[str, Any]:
        """
        Create a new airline record.
        
        Args:
            company_name: Name of the airline company
            
        Returns:
            Dictionary containing the created airline record
        """
        # Generate a new ID
        record_id = self.get_next_id()
        
        # Create a new airline record
        airline = AirlineRecord(
            record_id=record_id,
            company_name=company_name
        )
        
        # Convert to dictionary and add to records
        airline_dict = airline.to_dict()
        self.records.append(airline_dict)
        
        # Save to file
        self.save_to_file()
        
        return airline_dict
    
    def create_flight(self, client_id: int, airline_id: int,
                     date: datetime, start_city: str,
                     end_city: str) -> Dict[str, Any]:
        """
        Create a new flight record.
        
        Args:
            client_id: ID of the client taking the flight
            airline_id: ID of the airline operating the flight
            date: Date and time of the flight
            start_city: Departure city
            end_city: Destination city
            
        Returns:
            Dictionary containing the created flight record
        """
        # Verify that client and airline exist
        client_exists = any(r.get("id") == client_id and r.get("type") == "client" 
                          for r in self.records)
        airline_exists = any(r.get("id") == airline_id and r.get("type") == "airline"
                           for r in self.records)
        
        if not client_exists:
            raise ValueError(f"Client with ID {client_id} does not exist")
        
        if not airline_exists:
            raise ValueError(f"Airline with ID {airline_id} does not exist")
        
        # Generate a new ID
        record_id = self.get_next_id()
        
        # Create a new flight record
        flight = FlightRecord(
            record_id=record_id,
            client_id=client_id,
            airline_id=airline_id,
            date=date,
            start_city=start_city,
            end_city=end_city
        )
        
        # Convert to dictionary and add to records
        flight_dict = flight.to_dict()
        self.records.append(flight_dict)
        
        # Save to file
        self.save_to_file()
        
        return flight_dict
    
    def get_record_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a record by its ID.
        
        Args:
            record_id: ID of the record to retrieve
            
        Returns:
            Record dictionary if found, None otherwise
        """
        for record in self.records:
            if record.get("id") == record_id:
                return record
        return None
    
    def get_records_by_type(self, record_type: str) -> List[Dict[str, Any]]:
        """
        Retrieve all records of a specific type.
        
        Args:
            record_type: Type of records to retrieve ('client', 'airline', or 'flight')
            
        Returns:
            List of record dictionaries of the specified type
        """
        return [record for record in self.records if record.get("type") == record_type]
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """
        Retrieve all records in the system.
        
        Returns:
            List of all record dictionaries
        """
        return self.records
    
    def update_record(self, record_id: int, updated_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a record with new data.
        
        Args:
            record_id: ID of the record to update
            updated_data: Dictionary containing the fields to update
            
        Returns:
            Updated record dictionary if successful, None if record not found
            
        Raises:
            ValueError: If validation fails
        """
        # Find the record
        record_index = None
        for i, record in enumerate(self.records):
            if record.get("id") == record_id:
                record_index = i
                break
        
        if record_index is None:
            return None
        
        # Get the record and its type
        record = self.records[record_index]
        record_type = record.get("type")
        
        # Create a copy of the record with updates
        updated_record = record.copy()
        updated_record.update(updated_data)
        
        # Validate the updated record
        errors = {}
        if record_type == "client":
            errors = validate_client_record(updated_record)
        elif record_type == "airline":
            errors = validate_airline_record(updated_record)
        elif record_type == "flight":
            # Convert string date to datetime if necessary
            if "date" in updated_data and isinstance(updated_data["date"], str):
                try:
                    updated_data["date"] = datetime.fromisoformat(updated_data["date"])
                    updated_record["date"] = updated_data["date"]
                except ValueError:
                    errors["date"] = "Invalid date format"
            
            # Check referential integrity
            if "client_id" in updated_data:
                client_exists = any(r.get("id") == updated_data["client_id"] and 
                                r.get("type") == "client" for r in self.records)
                if not client_exists:
                    errors["client_id"] = f"Client with ID {updated_data['client_id']} does not exist"
            
            if "airline_id" in updated_data:
                airline_exists = any(r.get("id") == updated_data["airline_id"] and 
                                r.get("type") == "airline" for r in self.records)
                if not airline_exists:
                    errors["airline_id"] = f"Airline with ID {updated_data['airline_id']} does not exist"
            
            if not errors:
                errors = validate_flight_record(updated_record)
        
        # If there are validation errors, raise an exception
        if errors:
            error_msg = "; ".join(f"{key}: {value}" for key, value in errors.items())
            raise ValueError(f"Validation errors: {error_msg}")
        
        # Update the record
        self.records[record_index] = updated_record
        
        # Save to file
        self.save_to_file()
        
        return updated_record
    
    def delete_record(self, record_id: int) -> bool:
        """
        Delete a record by ID.
        
        Args:
            record_id: ID of the record to delete
            
        Returns:
            True if successful, False if record not found or can't be deleted
            
        Raises:
            ValueError: If the record is referenced by other records
        """
        # Find the record
        record_index = None
        record_type = None
        for i, record in enumerate(self.records):
            if record.get("id") == record_id:
                record_index = i
                record_type = record.get("type")
                break
        
        if record_index is None:
            return False
        
        # Check if record can be deleted
        if record_type == "client":
            # Check if any flight references this client
            referenced = any(r.get("type") == "flight" and r.get("client_id") == record_id 
                        for r in self.records)
            if referenced:
                raise ValueError(f"Cannot delete client with ID {record_id} because it is referenced by flight records")
        
        elif record_type == "airline":
            # Check if any flight references this airline
            referenced = any(r.get("type") == "flight" and r.get("airline_id") == record_id 
                        for r in self.records)
            if referenced:
                raise ValueError(f"Cannot delete airline with ID {record_id} because it is referenced by flight records")
        
        # Delete the record
        del self.records[record_index]
        
        # Save to file
        self.save_to_file()
        
        return True
