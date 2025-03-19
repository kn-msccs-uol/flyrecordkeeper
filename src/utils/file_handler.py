"""
File handler module for FlyRecordKeeper.

This module provides functionality for loading and saving records
to and from JSON files.
"""
import json
import os
from typing import List, Dict, Any, Union
from datetime import datetime

# Import the record classes
from models.client_record import ClientRecord
from models.airline_record import AirlineRecord
from models.flight_record import FlightRecord


def load_records(filename: str) -> List[Dict[str, Any]]:
    """
    Load records from a JSON file.
    
    Args:
        filename: Path to the JSON file
        
    Returns:
        List of dictionaries representing records, empty list if file doesn't exist
        
    Raises:
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, 'r') as file:
            records = json.load(file)
            return records
    except json.JSONDecodeError as e:
        print(f"Error loading records: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error loading records: {e}")
        return []


def save_records(clients: List[ClientRecord], airlines: List[AirlineRecord], flights: List[FlightRecord], filename: str) -> bool:
    """
    Save records to a JSON file.
    
    Args:
        records: List of record dictionaries to save
        filename: Path to the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as file:
            json.dump(records, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving records: {e}")
        return False


def dict_to_record(record_dict: Dict[str, Any]) -> Union[ClientRecord, AirlineRecord, FlightRecord, None]:
    """
    Convert a dictionary to the appropriate record object.

    While the system primarily stores and manipulates records as dictionaries,
    this function allows conversion to objects when OO functionality is needed
    (such as for UI display or specialized processing).
    
    Args:
        record_dict: Dictionary containing record data
        
    Returns:
        Record object of appropriate type, or None if type is unknown
    """
    record_type = record_dict.get("type", "")
    record_classes = {
        "client": ClientRecord,
        "airline": AirlineRecord,
        "flight": FlightRecord
    }

    if record_type in record_classes:
        # Handle date conversion for flight records
        if record_type == "flight" and "date" in record_dict and isinstance(record_dict["date"], str):
            # Convert date string to datetime object before passing to FlightRecord
            record_dict["date"] = datetime.fromisoformat(record_dict["date"])
        
        return record_classes[record_type].from_dict(record_dict)
    else:
        print(f"Unknown record type: {record_type}")
        return None
