"""
Search Controller module for FlyRecordKeeper.

This module provides centralized search functionality across all record types,
allowing for flexible and consistent searching throughout the application.

This follows the MVC (Model-View-Controller) design pattern where:
1. Model: Record classes and RecordManager
2. View: GUI components  
3. Controller: This module - provides specialised search capabilities
"""

import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from models.record_manager import RecordManager
from models.base_record import BaseRecord


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

    def parse_search_query(self, query: str) -> List[str]:
        """
        Parse a search query into individual search terms.
        
        Args:
            query: The search query string
            
        Returns:
            List of individual search terms
        """
        if not query or not query.strip():
            return []
            
        # Split by commas or spaces and remove empty terms
        terms = [term.strip() for term in re.split(r'[,\s]+', query) if term.strip()]
        return terms
    
    def search_clients(self, search_query: str) -> List[BaseRecord]:
        """
        Search for clients matching the given query.
        
        The search supports:
        - Partial matches on client ID, name, country or phone number
        - Multiple search terms (combined with AND logic)
        
        Args:
            query: Search query string
            
        Returns:
            List of client records matching the search criteria
        """
        # Parse the query into search terms
        search_terms = self.parse_search_query(search_query)
        
        # Get all client records
        all_clients = self.record_manager.get_records_by_type('client')
        
        # If no search terms, return all clients
        if not search_terms:
            return all_clients
            
        # Filter clients based on search terms
        search_results = all_clients
        for term in search_terms:
            # Filter results for this term
            term_results = []
            for client in search_results:
                # Check if term matches ID, name, country or phone number
                id_match = term in str(client.id)
                name_match = term.lower() in client.name.lower()
                country_match = term.lower() in client.country.lower()
                phone_match = term in str(client.phone_number)
                
                if id_match or name_match or country_match or phone_match:
                    term_results.append(client)
            search_results = term_results
            
        return search_results

    def search_airlines(self, search_query: str) -> List[BaseRecord]:
        """
        Search for airlines matching the given query.
        
        The search supports:
        - Partial matches on airline ID or company name
        - Multiple search terms (combined with AND logic)
        
        Args:
            query: Search query string
            
        Returns:
            List of airline records matching the search criteria
        """
        # Parse the query into search terms
        search_terms = self.parse_search_query(search_query)

        # Get all airline records
        all_airlines = self.record_manager.get_records_by_type('airline')
        
        # If no search terms, return all airlines
        if not search_terms:
            return all_airlines
            
        # Filter airlines based on search terms
        search_results = all_airlines
        for term in search_terms:
            # Filter results for this term
            term_results = []
            for airline in search_results:
                # Check if term matches ID or company name
                id_match = term in str(airline.id)
                name_match = term.lower() in airline.company_name.lower()

                if id_match or name_match:
                    term_results.append(airline)
            search_results = term_results
            
        return search_results
    
    def search_flights(self, search_query: str) -> List[BaseRecord]:
        """
        Search for flights matching the given query.
        
        The search supports:
        - Partial matches on flight ID, client ID, client name, client phone number, airline ID,
          airline name, date, start city, or end city
        - Multiple search terms (combined with AND logic)
        
        Args:
            query: Search query string
            
        Returns:
            List of flight records matching the search criteria
        """
        # Parse the query into search terms
        search_terms = self.parse_search_query(search_query)
        
        # Get all flight records
        all_flights = self.record_manager.get_records_by_type('flight')
        
        # If no search terms, return all flights
        if not search_terms:
            return all_flights
            
        # Filter flights based on search terms
        search_results = all_flights
        for term in search_terms:
            # Filter results for this term
            term_results = []
            for flight in search_results:
                # Check if term matches flight ID, client ID, client name, client phone number,
                # airline ID, airline name, start city, or end city
                id_match = term in str(flight.id)
                client_id_match = term in str(flight.client_id)
                airline_id_match = term in str(flight.airline_id)
                start_city_match = term.lower() in flight.start_city.lower()
                end_city_match = term.lower() in flight.end_city.lower()

                # Also check client and airline name matches
                client_name_match = False
                try:
                    client = self.record_manager.get_record_by_id(flight.client_id, "client")
                    client_name_match = term.lower() in client.name.lower()
                except:
                    pass

                airline_name_match = False
                try:
                    airline = self.record_manager.get_record_by_id(flight.airline_id, "airline")
                    airline_name_match = term.lower() in airline.company_name.lower()
                except:
                    pass
                
                # Also check date matches (partial string in ISO format)
                date_match = False
                if hasattr(flight, 'date'):
                    try:
                        date_str = flight.date.isoformat()
                        date_match = term in date_str
                    except:
                        pass
                
                if (id_match or client_id_match or client_name_match or airline_id_match or 
                    airline_name_match or start_city_match or end_city_match or date_match):
                    term_results.append(flight)
            search_results = term_results
            
        return search_results
