"""
Search Controller module for FlyRecordKeeper.

This module provides centralized search functionality across all record types,
allowing for flexible and consistent searching throughout the application.

This follows the MVC (Model-View-Controller) design pattern where:
1. Model: Record classes and RecordManager
2. View: GUI components
3. Controller: This module - provides generic search capabilities
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from models.record_manager import RecordManager


class SearchController:
    """
    Controller class for search operations across all record types.
    
    Provides comprehensive search functionality with a generic core
    that can be tailored for specific entity types.
    """
    
    def __init__(self, record_manager: RecordManager = None):
        """
        Initialize a new SearchController instance.
        
        Args:
            record_manager: RecordManager instance, creates a new one if None
        """
        self.record_manager = record_manager or RecordManager()
    
    def _generic_search(self, records: List[Dict[str, Any]], **criteria) -> List[Dict[str, Any]]:
        """
        Generic search method that filters records based on multiple criteria.
        
        Args:
            records: List of records to search through
            **criteria: Key-value pairs where key is field name and value is search value
            
        Returns:
            List of records matching all provided criteria
        """
        # If no criteria provided, return all records
        if not any(v is not None for v in criteria.values()):
            return records
            
        results = []
        
        for record in records:
            match = True
            
            for field, value in criteria.items():
                if value is None:
                    continue  # Skip None values
                    
                # Handle ID fields (exact match)
                if field.endswith('_id') and isinstance(value, int):
                    if record.get(field) != value:
                        match = False
                        break
                        
                # Handle string fields (partial match)
                elif isinstance(value, str) and field in record:
                    if value.lower() not in str(record.get(field, "")).lower():
                        match = False
                        break
                        
                # Handle date field
                elif field == "date" and "date" in record:
                    record_date = None
                    
                    # Convert string date to datetime if needed
                    if isinstance(record["date"], str):
                        try:
                            record_date = datetime.fromisoformat(record["date"])
                        except ValueError:
                            match = False
                            break
                    else:
                        record_date = record["date"]
                        
                    # Check if dates match (comparing only date part, not time)
                    if record_date.date() != value.date():
                        match = False
                        break
                        
                # Handle date range
                elif field == "date_range" and "date" in record:
                    start_date, end_date = value
                    record_date = None
                    
                    # Convert string date to datetime if needed
                    if isinstance(record["date"], str):
                        try:
                            record_date = datetime.fromisoformat(record["date"])
                        except ValueError:
                            match = False
                            break
                    else:
                        record_date = record["date"]
                        
                    # Check if date is in range
                    if not (start_date <= record_date <= end_date):
                        match = False
                        break
                        
                # Handle other fields (exact match)
                elif field in record and record.get(field) != value:
                    match = False
                    break
            
            if match:
                results.append(record)
                
        return results
    
    def search_clients(self, client_id: int = None, name: str = None, 
                       phone_number: str = None) -> List[Dict[str, Any]]:
        """
        Search for clients by ID, name, or phone number.
        
        Args:
            client_id: Client ID to search for (optional)
            name: Client name or partial name to search for (optional)
            phone_number: Phone number or partial number to search for (optional)
            
        Returns:
            List of client records matching the search criteria
        """
        clients = self.record_manager.get_records_by_type("client")
        return self._generic_search(
            clients, 
            id=client_id,
            name=name, 
            phone_number=phone_number
        )
    
    def search_airlines(self, airline_id: int = None, 
                        company_name: str = None) -> List[Dict[str, Any]]:
        """
        Search for airlines by ID or company name.
        
        Args:
            airline_id: Airline ID to search for (optional)
            company_name: Company name or partial name to search for (optional)
            
        Returns:
            List of airline records matching the search criteria
        """
        airlines = self.record_manager.get_records_by_type("airline")
        return self._generic_search(
            airlines, 
            id=airline_id,
            company_name=company_name
        )
    
    def search_flights(self, flight_id: int = None, client_id: int = None, 
                      client_name: str = None, client_phone: str = None,
                      airline_id: int = None, airline_name: str = None,
                      date: datetime = None, date_range: tuple = None,
                      start_city: str = None, end_city: str = None) -> List[Dict[str, Any]]:
        """
        Search for flights with comprehensive criteria.
        
        Args:
            flight_id: Flight ID to search for (optional)
            client_id: Client ID to filter by (optional)
            client_name: Client name to search for (optional)
            client_phone: Client phone number to search for (optional)
            airline_id: Airline ID to filter by (optional)
            airline_name: Airline company name to search for (optional)
            date: Exact date to match (optional)
            date_range: Tuple of (start_date, end_date) to filter by (optional)
            start_city: Departure city to search for (optional)
            end_city: Destination city to search for (optional)
            
        Returns:
            List of flight records matching all specified search criteria
        """
        # Find clients by name or phone if provided
        if client_name or client_phone:
            matching_clients = self.search_clients(
                name=client_name, 
                phone_number=client_phone
            )
            
            if matching_clients:
                client_ids = [c["id"] for c in matching_clients]
                
                # If specific client ID was also provided, find intersection
                if client_id and client_id not in client_ids:
                    return []  # No matches
                    
                # Otherwise use the found client IDs
                client_id = client_ids
            elif client_name or client_phone:
                return []  # No matching clients found
        
        # Find airlines by name if provided
        if airline_name:
            matching_airlines = self.search_airlines(company_name=airline_name)
            
            if matching_airlines:
                airline_ids = [a["id"] for a in matching_airlines]
                
                # If specific airline ID was also provided, find intersection
                if airline_id and airline_id not in airline_ids:
                    return []  # No matches
                    
                # Otherwise use the found airline IDs
                airline_id = airline_ids
            elif airline_name:
                return []  # No matching airlines found
        
        # Get all flights
        flights = self.record_manager.get_records_by_type("flight")
        
        # Use generic search with all remaining criteria
        return self._generic_search(
            flights,
            id=flight_id,
            client_id=client_id,
            airline_id=airline_id,
            date=date,
            date_range=date_range,
            start_city=start_city,
            end_city=end_city
        )
