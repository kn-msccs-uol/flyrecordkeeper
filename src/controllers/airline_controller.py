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
from controllers.search_controller import SearchController


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
    
    def search_airlines(self, search_term: str = None, airline_id: int = None,
                        company_name: str = None) -> List[Dict[str, Any]]:
        """
        Search for airlines by ID or company name.
        
        Args:
            search_term: General term to search in company name (optional)
            airline_id: Airline ID to search for (optional)
            company_name: Company name to search for (optional)
            
        Returns:
            List of airline records matching the search criteria
        """
        search_controller = SearchController(self.record_manager)
        
        # If general search term is provided, use it for company name
        if search_term:
            company_name = search_term
        
        return search_controller.search_airlines(
            airline_id=airline_id,
            company_name=company_name
        )
