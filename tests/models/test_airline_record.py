import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from models.airline_record import AirlineRecord

class TestAirlineRecord(unittest.TestCase):

    #Set up of sample data
    def setUp(self):
        self.sample_data = {
            "id": 1,
            "company_name": "British Airways"
        }
        self.airline = AirlineRecord(self.sample_data["id"], self.sample_data["company_name"])

    #Test coversion to dictionary type
    def test_to_dict(self):
        airline_dict = self.airline.to_dict()
        self.assertEqual(airline_dict["id"], self.sample_data["id"])
        self.assertEqual(airline_dict["company_name"], self.sample_data["company_name"])

    #Test creation from dictionary type
    def test_from_dict(self):
        airline = AirlineRecord.from_dict(self.sample_data)
        self.assertEqual(airline.id, self.sample_data["id"])
        self.assertEqual(airline.company_name, self.sample_data["company_name"])

    #Test validation of sample data
    def test_validation_success(self):
        errors = AirlineRecord.validate(self.sample_data)
        self.assertEqual(errors, {})

    def test_validation_missing_company_name(self):
        invalid_data = self.sample_data.copy()
        del invalid_data["company_name"]
        errors = AirlineRecord.validate(invalid_data)
        self.assertIn("company_name", errors)

if __name__ == "__main__":
    unittest.main()
