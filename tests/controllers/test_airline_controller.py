import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from unittest.mock import MagicMock
from controllers.airline_controller import AirlineController
from models.record_manager import RecordManager

class TestAirlineController(unittest.TestCase):

    def setUp(self):
        self.mock_record_manager = MagicMock(spec=RecordManager)
        self.controller = AirlineController(record_manager=self.mock_record_manager)

    def test_get_all_airlines(self):
        self.mock_record_manager.get_records_by_type.return_value = [
            {"id": 1, "company_name": "Airline A"},
            {"id": 2, "company_name": "Airline B"}
        ]
        result = self.controller.get_all_airlines()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["company_name"], "Airline A")
        self.mock_record_manager.get_records_by_type.assert_called_once_with("airline")

    def test_get_airline_found(self):
        self.mock_record_manager.get_record_by_id.return_value = {"id": 1, "type": "airline",
                                                                  "company_name": "Airline A"}
        result = self.controller.get_airline(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["company_name"], "Airline A")
        self.mock_record_manager.get_record_by_id.assert_called_once_with(1)

    def test_get_airline_not_found(self):
        self.mock_record_manager.get_record_by_id.return_value = None
        result = self.controller.get_airline(999)
        self.assertIsNone(result)

    def test_create_airline(self):
        self.mock_record_manager.create_record.return_value = {"id": 1, "company_name": "New Airline"}
        result = self.controller.create_airline("New Airline")
        self.assertEqual(result["company_name"], "New Airline")
        self.mock_record_manager.create_record.assert_called_once_with("airline", {"company_name": "New Airline"})

    def test_update_airline_success(self):
        self.mock_record_manager.get_record_by_id.return_value = {"id": 1, "type": "airline",
                                                                  "company_name": "Old Airline"}
        self.mock_record_manager.update_record.return_value = {"id": 1, "company_name": "Updated Airline"}
        result = self.controller.update_airline(1, company_name="Updated Airline")
        self.assertEqual(result["company_name"], "Updated Airline")
        self.mock_record_manager.update_record.assert_called_once_with(1, {"company_name": "Updated Airline"})

    def test_update_airline_not_found(self):
        self.mock_record_manager.get_record_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.controller.update_airline(999, company_name="Updated Airline")
        self.assertTrue("Airline with ID 999 not found" in str(context.exception))

    def test_delete_airline_success(self):
        self.mock_record_manager.get_record_by_id.return_value = {"id": 1, "type": "airline",
                                                                  "company_name": "Airline A"}
        self.mock_record_manager.delete_record.return_value = True
        result = self.controller.delete_airline(1)
        self.assertTrue(result)
        self.mock_record_manager.delete_record.assert_called_once_with(1)

    def test_delete_airline_not_found(self):
        self.mock_record_manager.get_record_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.controller.delete_airline(999)
        self.assertTrue("Airline with ID 999 not found" in str(context.exception))

    def test_search_airlines(self):
        self.mock_record_manager.get_records_by_type.return_value = [
            {"id": 1, "company_name": "British Airways"},
            {"id": 2, "company_name": "American Airlines"},
            {"id": 3, "company_name": "Lufthansa"}
        ]
        result = self.controller.search_airlines("air")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["company_name"], "British Airways")
        self.assertEqual(result[1]["company_name"], "American Airlines")


if __name__ == "__main__":
    unittest.main()
