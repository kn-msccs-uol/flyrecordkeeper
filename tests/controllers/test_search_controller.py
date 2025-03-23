import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import unittest
from unittest.mock import MagicMock
from datetime import datetime
from controllers.search_controller import SearchController

class DummyRecord:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class TestSearchController(unittest.TestCase):

    def setUp(self):
        # Setup dummy data
        self.dummy_clients = [
            DummyRecord(id=1, name="Kevin", country="UK", phone_number="12345"),
            DummyRecord(id=2, name="Alice", country="USA", phone_number="67890"),
        ]

        self.dummy_airlines = [
            DummyRecord(id=10, company_name="SkyHigh Airways"),
            DummyRecord(id=11, company_name="TestFlights Ltd"),
        ]

        self.dummy_flights = [
            DummyRecord(
                id=100,
                client_id=1,
                airline_id=10,
                start_city="London",
                end_city="Barcelona",
                date=datetime.fromisoformat("2025-03-23T14:00:00")
            ),
            DummyRecord(
                id=101,
                client_id=2,
                airline_id=11,
                start_city="New York",
                end_city="Paris",
                date=datetime.fromisoformat("2025-04-01T09:30:00")
            )
        ]

        # Mock record manager
        self.mock_record_manager = MagicMock()
        self.mock_record_manager.get_records_by_type.side_effect = lambda record_type: {
            "client": self.dummy_clients,
            "airline": self.dummy_airlines,
            "flight": self.dummy_flights
        }[record_type]

        self.mock_record_manager.get_record_by_id.side_effect = lambda record_id, record_type: {
            (1, "client"): self.dummy_clients[0],
            (2, "client"): self.dummy_clients[1],
            (10, "airline"): self.dummy_airlines[0],
            (11, "airline"): self.dummy_airlines[1]
        }[(record_id, record_type)]

        self.controller = SearchController(record_manager=self.mock_record_manager)

    def test_parse_search_query(self):
        query = "Kevin, UK"
        terms = self.controller.parse_search_query(query)
        self.assertEqual(terms, ["Kevin", "UK"])

    def test_search_clients_by_name(self):
        results = self.controller.search_clients("Kevin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Kevin")

    def test_search_clients_by_country(self):
        results = self.controller.search_clients("USA")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].country, "USA")

    def test_search_airlines_by_company_name(self):
        results = self.controller.search_airlines("SkyHigh")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].company_name, "SkyHigh Airways")

    def test_search_flights_by_start_city(self):
        results = self.controller.search_flights("London")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].start_city, "London")

    def test_search_flights_by_client_name(self):
        results = self.controller.search_flights("Kevin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 100)

    def test_search_flights_by_airline_name(self):
        results = self.controller.search_flights("SkyHigh")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 100)

    def test_search_flights_by_date(self):
        results = self.controller.search_flights("2025-03-23")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 100)

if __name__ == '__main__':
    unittest.main()
