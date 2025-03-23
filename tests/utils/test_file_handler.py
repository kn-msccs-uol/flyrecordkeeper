import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import unittest
import os
import json
import tempfile
from datetime import datetime
from utils import file_handler

class DummyClientRecord:
    @staticmethod
    def from_dict(data):
        return data

class DummyAirlineRecord:
    @staticmethod
    def from_dict(data):
        return data

class DummyFlightRecord:
    @staticmethod
    def from_dict(data):
        return data

# Patch the actual classes with dummy ones for testing
file_handler.ClientRecord = DummyClientRecord
file_handler.AirlineRecord = DummyAirlineRecord
file_handler.FlightRecord = DummyFlightRecord

class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.test_data = [
            {"type": "client", "name": "Kevin"},
            {"type": "airline", "name": "AirTest"},
            {"type": "flight", "date": datetime.now().isoformat(), "destination": "Barcelona"}
        ]
        with open(self.temp_file.name, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_load_records_existing_file(self):
        records = file_handler.load_records(self.temp_file.name)
        self.assertIsInstance(records, list)
        self.assertEqual(len(records), 3)

    def test_load_records_nonexistent_file(self):
        # Patch new_from_template to return False
        file_handler.new_from_template = lambda x: False
        records = file_handler.load_records("nonexistent.json")
        self.assertEqual(records, [])

    def test_save_records_success(self):
        success = file_handler.save_records(self.test_data, self.temp_file.name)
        self.assertTrue(success)

    def test_save_records_invalid_path(self):
        # Try saving to a folder that likely doesn't exist and can't be created
        success = file_handler.save_records(self.test_data, "/invalid_path/test.json")
        self.assertFalse(success)

    def test_dict_to_record_client(self):
        record = file_handler.dict_to_record({"type": "client", "name": "Test"})
        self.assertEqual(record["name"], "Test")

    def test_dict_to_record_airline(self):
        record = file_handler.dict_to_record({"type": "airline", "name": "TestAir"})
        self.assertEqual(record["name"], "TestAir")

    def test_dict_to_record_flight_with_date(self):
        now = datetime.now()
        record_dict = {"type": "flight", "date": now.isoformat(), "destination": "Rome"}
        record = file_handler.dict_to_record(record_dict)
        self.assertEqual(record["destination"], "Rome")

    def test_dict_to_record_unknown(self):
        record = file_handler.dict_to_record({"type": "unknown"})
        self.assertIsNone(record)

if __name__ == '__main__':
    unittest.main()
