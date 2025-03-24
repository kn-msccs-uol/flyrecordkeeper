import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import unittest
from datetime import datetime, timedelta
from models.record_manager import RecordManager

class DummyClient:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.type = "client"
    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type}

class DummyAirline:
    def __init__(self, id, company_name):
        self.id = id
        self.company_name = company_name
        self.type = "airline"
    def to_dict(self):
        return {"id": self.id, "company_name": self.company_name, "type": self.type}

class DummyFlight:
    def __init__(self, id, client_id, airline_id, date, start_city, end_city):
        self.id = id
        self.client_id = client_id
        self.airline_id = airline_id
        self.date = date
        self.start_city = start_city
        self.end_city = end_city
        self.type = "flight"
    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "airline_id": self.airline_id,
            "date": self.date.isoformat(),
            "start_city": self.start_city,
            "end_city": self.end_city,
            "type": self.type
        }

class TestRecordManager(unittest.TestCase):

    def setUp(self):
        self.manager = RecordManager(filename="test_data.json")
        self.manager.clients = [DummyClient(1, "Kevin")]
        self.manager.airlines = [DummyAirline(1, "SkyHigh")]
        self.manager.flights = [
            DummyFlight(1, 1, 1, datetime.now() + timedelta(days=1), "London", "Barcelona")
        ]

    def test_get_next_id(self):
        self.assertEqual(self.manager.get_next_id("client"), 2)
        self.assertEqual(self.manager.get_next_id("airline"), 2)
        self.assertEqual(self.manager.get_next_id("flight"), 2)

    def test_get_record_by_id(self):
        client = self.manager.get_record_by_id(1, "client")
        self.assertEqual(client.name, "Kevin")

    def test_get_records_by_type(self):
        clients = self.manager.get_records_by_type("client")
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0].name, "Kevin")

    def test_get_related_records(self):
        related = self.manager.get_related_records(1, "client")
        self.assertEqual(len(related), 1)
        self.assertEqual(related[0].start_city, "London")

    def test_check_can_delete(self):
        can_delete, reason = self.manager.check_can_delete(1, "client")
        self.assertFalse(can_delete)
        self.assertIn("referenced", reason)

    def test_delete_flight(self):
        # First, ensure deletion is possible (no relationships to check)
        self.manager.flights = [DummyFlight(2, 1, 1, datetime.now() + timedelta(days=1), "Paris", "Rome")]
        result = self.manager.delete_record(2, "flight")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.flights), 0)

if __name__ == '__main__':
    unittest.main()
