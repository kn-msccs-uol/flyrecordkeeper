"""
Record Manager module for FlyRecordKeeper.

This module provides functionality for creating, reading, updating,
and deleting (CRUD) records in the system.

This project uses a "Structured Dictionaries with OO Benefits" approach where:
1. Records are stored as dictionaries for serialization and storage
2. Classes provide structure, validation, and object-oriented functionality
3. The system maintains the benefits of both approaches
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import the record classes
from models.client_record import ClientRecord
from models.airline_record import AirlineRecord
from models.flight_record import FlightRecord

# Import the file handler
from utils.file_handler import load_records, save_records

# Import the validator
from utils.validators import get_validation_errors_summary


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
        self.clients = []
        self.airlines = []
        self.flights = []
        self.load_from_file()
    
    def load_from_file(self) -> bool:
        """
        Load records from the JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = load_records(self.filename)
            
            return self.from_json(data)
        except Exception as e:
            print('in load from file exception')
            print(self.clients)
            print(self.flights)
            print(self.airlines)
            print(f"Error loading records: {e}")
            return False
    
    def from_json(self, data) -> bool:
        self.clients = []
        self.airlines = []
        self.flights = []
        
        for rec in data["clients"]:
            self.clients.append(ClientRecord.from_dict(rec))
        for rec in data["airlines"]:
            self.airlines.append(AirlineRecord.from_dict(rec))
        for rec in data["flights"]:
            self.flights.append(FlightRecord.from_dict(rec))

        return True
    
    def save_to_file(self) -> bool:
        """
        Save records to the JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        return save_records(self.clients, self.airlines, self.flights, self.filename)
    
    def get_next_id(self, record_type: str) -> int:
        """
        Generate the next available record ID.
        
        Returns:
            Next available ID
        """
        if record_type == 'clients':
            if not self.clients:
                return 1
        
            return self.get_max(self.clients) + 1
        elif record_type == 'airlines':
            if not self.airlines:
                return 1
        
            return self.get_max(self.airlines) + 1
        elif record_type == 'flights':
            if not self.flights:
                return 1
        
            return self.get_max(self.flights) + 1
        
        return 0

    
    def get_max(self, list):
        max_id = 0
        for record in list:
            if "id" in record and record["id"] > max_id:
                max_id = record["id"]

        return max_id                

    def _get_validator_for_type(self, record_type: str):
        """
        Get the appropriate validator class for a record type.
        
        Args:
            record_type: Type of record ('client', 'airline', or 'flight')
            
        Returns:
            Appropriate validator class
            
        Raises:
            ValueError: If record type is unknown
        """
        if record_type == "client":
            return ClientRecord
        elif record_type == "airline":
            return AirlineRecord
        elif record_type == "flight":
            return FlightRecord
        else:
            raise ValueError(f"Unknown record type: {record_type}")
    
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
        # Create a new client record with all the fields
        client_data = {
            "name": name,
            "address_line1": address_line1,
            "address_line2": address_line2,
            "address_line3": address_line3,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country,
            "phone_number": phone_number
        }
        
        return self.create_record("client", client_data)
    
    def create_airline(self, company_name: str) -> Dict[str, Any]:
        """
        Create a new airline record.
        
        Args:
            company_name: Name of the airline company
            
        Returns:
            Dictionary containing the created airline record
        """        
        # Create a new airline record
        airline_data = {
            "company_name": company_name
        }
        
        return self.create_record("airline", airline_data)
    
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
        # Create a new flight record
        flight_data = {
            "client_id": client_id,
            "airline_id": airline_id,
            "date": date,
            "start_city": start_city,
            "end_city": end_city
        }
        
        return self.create_record("flight", flight_data)
    
    def get_record_by_id(self, record_id: int, record_type: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a record by its ID.
        
        Args:
            record_id: ID of the record to retrieve
            
        Returns:
            Record dictionary if found, None otherwise
        """
        rec = None

        if record_type == "client":
            rec = [item for item in self.clients if item['ID'] == record_id]
        elif record_type == "airline":
            rec = [item for item in self.airlines if item['ID'] == record_id]
        elif record_type == "flight":
            rec = [item for item in self.flights if item['ID'] == record_id]
        else:
            raise ValueError(f"Unknown record type: {record_type}")

        if len(rec) > 0:
            raise ValueError(f"Unknown records of type({record_type}) found for ID({record_id})")

        return rec
    
    
    def get_records_by_type(self, record_type: str) -> List[Dict[str, Any]]:
        """
        Retrieve all records of a specific type.
        
        Args:
            record_type: Type of records to retrieve ('client', 'airline', or 'flight')
            
        Returns:
            List of record dictionaries of the specified type
        """
        #return [record for record in self.records if record.get("type") == record_type]
        if record_type == "client":
            return self.clients
        elif record_type == "airline":
            return self.airlines
        elif record_type == "flight":
            return self.flights
        else:
            raise ValueError(f"Unknown record type: {record_type}")

    
    def get_related_records(self, record_id: int, record_type: str) -> List[Dict[str, Any]]:
        """
        Get all records that relate to a specific record.
        
        Args:
            record_id: ID of the reference record
            record_type: Type of the reference record ('client' or 'airline')
            
        Returns:
            List of records that reference this record
        """
        related_records = []
        
        if record_type == "client":
            # Find flights that reference this client
            related_records = [r for r in self.flights 
                            if r.get("client_id") == record_id]
        
        elif record_type == "airline":
            # Find flights that reference this airline
            related_records = [r for r in self.flights 
                            if r.get("airline_id") == record_id]
        
        return related_records
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """
        Retrieve all records in the system.
        
        Returns:
            List of all record dictionaries
        """
        all_recs = []
        all_recs.append(self.clients)
        all_recs.append(self.airlines)
        all_recs.append(self.flights)

        return all_recs
    
    def create_record(self, record_type: str, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record with validation and relationship checking.
        
        Args:
            record_type: Type of record to create ('client', 'airline', or 'flight')
            record_data: Dictionary containing the record data
            
        Returns:
            Newly created record dictionary
            
        Raises:
            ValueError: If validation fails
        """
        
        # Generate a new ID
        record_id = self.get_next_id()
        record_data["id"] = record_id
        record_data["type"] = record_type
        
        # Handle date conversion for flight records
        if record_type == "flight" and "date" in record_data and isinstance(record_data["date"], str):
            try:
                record_data["date"] = datetime.fromisoformat(record_data["date"])
            except ValueError:
                raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        
        # Validate based on record type
        errors = {}
        validator_class = self._get_validator_for_type(record_type)
        errors = validator_class.validate(record_data, self.flights if record_type == "flight" else None)
        
        # If there are validation errors, raise an exception
        if errors:
            error_msg = get_validation_errors_summary(errors)
            raise ValueError(f"Validation errors: {error_msg}")
        
        # Create the record
        self.records.append(record_data)
        
        # Save to file
        self.save_to_file()
        
        return record_data
    
    def update_record(self, record_id: int, updated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a record with validation and relationship checking.
        
        Args:
            record_id: ID of the record to update
            updated_data: Dictionary containing the fields to update
            
        Returns:
            Updated record dictionary if successful
            
        Raises:
            ValueError: If validation fails or if update would break referential integrity
        """
        
        # Find the record
        record = self.get_record_by_id(record_id)
        if not record:
            raise ValueError(f"Record with ID {record_id} not found")
        
        # Create a copy of the record with updates
        updated_record = record.copy()
        updated_record.update(updated_data)
        
        # Get record type
        record_type = record.get("type")
        
        # Handle date conversion for flight records
        if record_type == "flight" and "date" in updated_data and isinstance(updated_data["date"], str):
            try:
                updated_data["date"] = datetime.fromisoformat(updated_data["date"])
                updated_record["date"] = updated_data["date"]
            except ValueError:
                raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        
        # Validate based on record type
        errors = {}
        validator_class = self._get_validator_for_type(record_type)
        errors = validator_class.validate(updated_record, self.records if record_type == "flight" else None)
        
        # If there are validation errors, raise an exception
        if errors:
            error_msg = get_validation_errors_summary(errors)
            raise ValueError(f"Validation errors: {error_msg}")
        
        # Update the record in the records list
        for i, r in enumerate(self.records):
            if r.get("id") == record_id:
                self.records[i] = updated_record
                break
        
        # Save to file
        self.save_to_file()
        
        return updated_record
    
    def check_can_delete(self, record_id: int) -> tuple[bool, str]:
        """
        Check if a record can be safely deleted without breaking relationships.
        
        Args:
            record_id: ID of the record to check
            
        Returns:
            Tuple of (can_delete, reason) where reason explains why deletion is not allowed
        """
        # Find the record
        record = self.get_record_by_id(record_id)
        if not record:
            return False, f"Record with ID {record_id} not found"
        
        record_type = record.get("type")
        
        if record_type in ["client", "airline"]:
            related_records = self.get_related_records(record_id, record_type)
            if related_records:
                return False, f"Cannot delete {record_type} with ID {record_id} because it is referenced by {len(related_records)} flight records"
        
        return True, ""
    
    def delete_record(self, record_id: int) -> bool:
        """
        Delete a record by ID.
        
        Args:
            record_id: ID of the record to delete
            
        Returns:
            True if successful, False if record not found or can't be deleted
            
        Raises:
            ValueError: If the record is cannot be deleted
        """
        can_delete, reason = self.check_can_delete(record_id)

        if not can_delete:
            raise ValueError(reason)

        # Find the record index
        record_index = None
        for i, record in enumerate(self.records):
            if record.get("id") == record_id:
                record_index = i
                break
        
        if record_index is None:
            return False
        
        # Delete the record
        del self.records[record_index]
        
        # Save to file
        self.save_to_file()
        
        return True
