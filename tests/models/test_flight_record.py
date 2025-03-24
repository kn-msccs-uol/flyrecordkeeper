import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from datetime import datetime
from models.flight_record import FlightRecord

class TestFlightRecord(unittest.TestCase):

    def setUp(self):
        self.valid_obj = {
            "id": 1,
            "type": "flight",
            "client_id": 101,
            "airline_id": 202,
            "date": datetime(2025, 5, 1, 10, 0),
            "start_city": "London",
            "end_city": "New York"
        }

        self.valid_dict = {
            "id": 1,
            "type": "flight",
            "client_id": 101,
            "airline_id": 202,
            "date": "2025-05-01T10:00:00",
            "start_city": "London",
            "end_city": "New York"
        }

    def test_initialization(self):
        flight = FlightRecord(
            record_id=self.valid_obj["id"],
            client_id=self.valid_obj["client_id"],
            airline_id=self.valid_obj["airline_id"],
            date=datetime.fromisoformat(self.valid_obj["date"].isoformat()),
            start_city=self.valid_obj["start_city"],
            end_city=self.valid_obj["end_city"]
        )
        self.assertEqual(flight.id, 1)
        self.assertEqual(flight.type, "flight")
        self.assertEqual(flight.client_id, 101)
        self.assertEqual(flight.airline_id, 202)
        self.assertEqual(flight.date, datetime(2025, 5, 1, 10, 0))
        self.assertEqual(flight.start_city, "London")
        self.assertEqual(flight.end_city, "New York")

    def test_to_dict(self):
        flight = FlightRecord.from_dict(self.valid_dict)
        result = flight.to_dict()

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["client_id"], 101)
        self.assertEqual(result["airline_id"], 202)
        self.assertEqual(datetime.fromisoformat(result["date"]), datetime(2025, 5, 1, 10, 0))
        self.assertEqual(result["start_city"], "London")
        self.assertEqual(result["end_city"], "New York")

    def test_from_dict(self):
        flight = FlightRecord.from_dict(self.valid_dict)
        self.assertIsInstance(flight, FlightRecord)
        self.assertEqual(flight.date, datetime(2025, 5, 1, 10, 0))

    def test_validate_valid_data(self):
        errors = FlightRecord.validate(self.valid_obj)
        self.assertEqual(errors, {})  # No validation errors expected

    def test_validate_missing_field(self):
        invalid_data = self.valid_obj.copy()
        del invalid_data["start_city"]

        errors = FlightRecord.validate(invalid_data)
        self.assertIn("start_city", errors)
        self.assertIsInstance(errors["start_city"], str)
        self.assertGreater(len(errors["start_city"]), 0)

    def test_validate_relationships_fail(self):
        # Related records are missing client_id and airline_id
        all_records = [
            {"id": 999, "type": "client"},
            {"id": 888, "type": "airline"},
        ]

        errors = FlightRecord.validate(self.valid_obj, all_records=all_records)
        self.assertIn("client_id", errors)
        self.assertIn("airline_id", errors)
        self.assertIn("does not exist", errors["client_id"])
        self.assertIn("does not exist", errors["airline_id"])

    def test_validate_relationships_pass(self):
        # Related records include correct client and airline
        all_records = [
            {"id": 101, "type": "client"},
            {"id": 202, "type": "airline"},
        ]

        errors = FlightRecord.validate(self.valid_obj, all_records=all_records)
        self.assertEqual(errors, {})  # No relationship errors

if __name__ == "__main__":
    unittest.main()
