"""
Flight Controller module for FlyRecordKeeper.

This module provides controller functionality for flight record operations,
acting as an intermediary between the user interface and the data model.

This follows the MVC (Model-View-Controller) design pattern where:
1. Model: Record classes and RecordManager
2. View: GUI components
3. Controller: This module - translates UI actions to model operations
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from models.record_manager import RecordManager


class FlightController:
    """
    Controller class for flight record operations.
    
    Handles the business logic for creating, reading, updating, and deleting flight records.
    """
    
    def __init__(self, record_manager: RecordManager = None):
        """
        Initialize a new FlightController instance.
        
        Args:
            record_manager: RecordManager instance, creates a new one if None
        """
        self.record_manager = record_manager or RecordManager()
    
    def get_all_flights(self) -> List[Dict[str, Any]]:
        """
        Get all flight records.
        
        Returns:
            List of flight record dictionaries
        """
        return self.record_manager.get_records_by_type("flight")
    
    def get_flight(self, flight_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific flight record by ID.
        
        Args:
            flight_id: ID of the flight to retrieve
            
        Returns:
            Flight record dictionary if found, None otherwise
        """
        record = self.record_manager.get_record_by_id(flight_id)
        if record and record.get("type") == "flight":
            return record
        return None
    
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
            Newly created flight record dictionary
            
        Raises:
            ValueError: If flight creation fails validation
        """
        flight_data = {
            "client_id": client_id,
            "airline_id": airline_id,
            "date": date,
            "start_city": start_city,
            "end_city": end_city
        }
        
        return self.record_manager.create_record("flight", flight_data)
    
    def update_flight(self, flight_id: int, **update_data) -> Dict[str, Any]:
        """
        Update an existing flight record.
        
        Args:
            flight_id: ID of the flight to update
            **update_data: Fields to update and their new values
            
        Returns:
            Updated flight record dictionary
            
        Raises:
            ValueError: If flight update fails validation or flight not found
        """
        # Get the flight to ensure it exists and is the correct type
        flight = self.get_flight(flight_id)
        if not flight:
            raise ValueError(f"Flight with ID {flight_id} not found")
        
        # Update the flight record
        return self.record_manager.update_record(flight_id, update_data)
    
    def delete_flight(self, flight_id: int) -> bool:
        """
        Delete a flight record.
        
        Args:
            flight_id: ID of the flight to delete
            
        Returns:
            True if successfully deleted, False otherwise
            
        Raises:
            ValueError: If flight cannot be deleted
        """
        # Get the flight to ensure it exists and is the correct type
        flight = self.get_flight(flight_id)
        if not flight:
            raise ValueError(f"Flight with ID {flight_id} not found")
        
        # Delete the flight record
        return self.record_manager.delete_record(flight_id)
    
    def search_flights(self, search_term: str = None, client_id: int = None, 
                      airline_id: int = None, start_city: str = None, 
                      end_city: str = None) -> List[Dict[str, Any]]:
        """
        Search for flights with various criteria.
        
        Args:
            search_term: Term to search in cities (optional)
            client_id: Filter by client ID (optional)
            airline_id: Filter by airline ID (optional)
            start_city: Filter by departure city (optional)
            end_city: Filter by destination city (optional)
            
        Returns:
            List of flight records matching the search criteria
        """
        flights = self.get_all_flights()
        results = []
        
        # Convert search term to lowercase if provided
        search_term_lower = search_term.lower() if search_term else None
        
        for flight in flights:
            # Check all specified criteria
            match = True
            
            if client_id is not None and flight.get("client_id") != client_id:
                match = False
                
            if airline_id is not None and flight.get("airline_id") != airline_id:
                match = False
                
            if start_city is not None and flight.get("start_city") != start_city:
                match = False
                
            if end_city is not None and flight.get("end_city") != end_city:
                match = False
                
            if search_term_lower is not None:
                if (search_term_lower not in flight.get("start_city", "").lower() and
                    search_term_lower not in flight.get("end_city", "").lower()):
                    match = False
                    
            if match:
                results.append(flight)
                
        return results
    
    def get_flights_by_client(self, client_id: int) -> List[Dict[str, Any]]:
        """
        Get all flights for a specific client.
        
        Args:
            client_id: ID of the client
            
        Returns:
            List of flight records for the specified client
        """
        return self.search_flights(client_id=client_id)
    
    def get_flights_by_airline(self, airline_id: int) -> List[Dict[str, Any]]:
        """
        Get all flights for a specific airline.
        
        Args:
            airline_id: ID of the airline
            
        Returns:
            List of flight records for the specified airline
        """
        return self.search_flights(airline_id=airline_id)
