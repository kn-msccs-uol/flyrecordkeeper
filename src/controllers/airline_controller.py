"""
Airline Controller module for FlyRecordKeeper.

This module provides controller functionality for airline record operations,
acting as an intermediary between the user interface and the data model.

This follows the MVC (Model-View-Controller) design pattern where:
1. Model: Record classes and RecordManager
2. View: GUI components
3. Controller: This module - translates UI actions to model operations
"""

from typing import Dict, Any, List, Optional
from models.record_manager import RecordManager


class AirlineController:
    """
    Controller class for airline record operations.
    
    Handles the business logic for creating, reading, updating, and deleting airline records.
    """
    
    def __init__(self, record_manager: RecordManager = None):
        """
        Initialize a new AirlineController instance.
        
        Args:
            record_manager: RecordManager instance, creates a new one if None
        """
        self.record_manager = record_manager or RecordManager()
    
    def get_all_airlines(self) -> List[Dict[str, Any]]:
        """
        Get all airline records.
        
        Returns:
            List of airline record dictionaries
        """
        return self.record_manager.get_records_by_type("airline")
    
    def get_airline(self, airline_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific airline record by ID.
        
        Args:
            airline_id: ID of the airline to retrieve
            
        Returns:
            Airline record dictionary if found, None otherwise
        """
        record = self.record_manager.get_record_by_id(airline_id)
        if record and record.get("type") == "airline":
            return record
        return None
    
    def create_airline(self, company_name: str) -> Dict[str, Any]:
        """
        Create a new airline record.
        
        Args:
            company_name: Name of the airline company
            
        Returns:
            Newly created airline record dictionary
            
        Raises:
            ValueError: If airline creation fails validation
        """
        airline_data = {
            "company_name": company_name
        }
        return self.record_manager.create_record("airline", airline_data)
    
    def update_airline(self, airline_id: int, **update_data) -> Dict[str, Any]:
        """
        Update an existing airline record.
        
        Args:
            airline_id: ID of the airline to update
            **update_data: Fields to update and their new values
            
        Returns:
            Updated airline record dictionary
            
        Raises:
            ValueError: If airline update fails validation or airline not found
        """
        # Get the airline to ensure it exists and is the correct type
        airline = self.get_airline(airline_id)
        if not airline:
            raise ValueError(f"Airline with ID {airline_id} not found")
        
        # Update the airline record
        return self.record_manager.update_record(airline_id, update_data)
    
    def delete_airline(self, airline_id: int) -> bool:
        """
        Delete an airline record.
        
        Args:
            airline_id: ID of the airline to delete
            
        Returns:
            True if successfully deleted, False otherwise
            
        Raises:
            ValueError: If airline cannot be deleted (e.g., referenced by flights)
        """
        # Get the airline to ensure it exists and is the correct type
        airline = self.get_airline(airline_id)
        if not airline:
            raise ValueError(f"Airline with ID {airline_id} not found")
        
        # Delete the airline record
        return self.record_manager.delete_record(airline_id)
    
    def search_airlines(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for airlines by company name.
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of airline records matching the search term
        """
        search_term = search_term.lower()
        airlines = self.get_all_airlines()
        
        results = []
        for airline in airlines:
            # Search in company name
            if search_term in airline.get("company_name", "").lower():
                results.append(airline)
        
        return results
