"""
Client Controller module for FlyRecordKeeper.

This module provides controller functionality for client record operations,
acting as an intermediary between the user interface and the data model.

This follows the MVC (Model-View-Controller) design pattern where:
1. Model: Record classes and RecordManager
2. View: GUI components
3. Controller: This module - translates UI actions to model operations
"""

from typing import Dict, Any, List, Optional
from models.record_manager import RecordManager


class ClientController:
    """
    Controller class for client record operations.
    
    Handles the business logic for creating, reading, updating, and deleting client records.
    """
    
    def __init__(self, record_manager: RecordManager = None):
        """
        Initialize a new ClientController instance.
        
        Args:
            record_manager: RecordManager instance, creates a new one if None
        """
        self.record_manager = record_manager or RecordManager()
    
    def get_all_clients(self) -> List[Dict[str, Any]]:
        """
        Get all client records.
        
        Returns:
            List of client record dictionaries
        """
        return self.record_manager.get_records_by_type("client")
    
    def get_client(self, client_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific client record by ID.
        
        Args:
            client_id: ID of the client to retrieve
            
        Returns:
            Client record dictionary if found, None otherwise
        """
        record = self.record_manager.get_record_by_id(client_id)
        if record and record.get("type") == "client":
            return record
        return None
    
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
            Newly created client record dictionary
            
        Raises:
            ValueError: If client creation fails validation
        """
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

        return self.record_manager.create_record("client", client_data)
    
    def update_client(self, client_id: int, **update_data) -> Dict[str, Any]:
        """
        Update an existing client record.
        
        Args:
            client_id: ID of the client to update
            **update_data: Fields to update and their new values
            
        Returns:
            Updated client record dictionary
            
        Raises:
            ValueError: If client update fails validation or client not found
        """
        # Get the client to ensure it exists and is the correct type
        client = self.get_client(client_id)
        if not client:
            raise ValueError(f"Client with ID {client_id} not found")
        
        # Update the client record
        return self.record_manager.update_record(client_id, update_data)
    
    def delete_client(self, client_id: int) -> bool:
        """
        Delete a client record.
        
        Args:
            client_id: ID of the client to delete
            
        Returns:
            True if successfully deleted, False otherwise
            
        Raises:
            ValueError: If client cannot be deleted (e.g., referenced by flights)
        """
        # Get the client to ensure it exists and is the correct type
        client = self.get_client(client_id)
        if not client:
            raise ValueError(f"Client with ID {client_id} not found")
        
        # Delete the client record
        return self.record_manager.delete_record(client_id)
    
    def search_clients(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for clients by name or phone number.
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of client records matching the search term
        """
        search_term = search_term.lower()
        clients = self.get_all_clients()
        
        results = []
        for client in clients:
            # Search in name and phone number fields only
            if (search_term in client.get("name", "").lower() or
                search_term in client.get("phone_number", "").lower()):
                results.append(client)
        
        return results
