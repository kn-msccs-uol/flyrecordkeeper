import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from models.client_record import ClientRecord

class TestClientRecord(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            "record_id": 1,
            "name": "John Doe",
            "address_line1": "123 Main St",
            "address_line2": "Apt 4B",
            "address_line3": "Building 2",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "country": "USA",
            "phone_number": "+1234567890"
        }
        self.client = ClientRecord(**self.sample_data)

    def test_to_dict(self):
        client_dict = self.client.to_dict()
        self.assertEqual(client_dict["name"], self.sample_data["name"])
        self.assertEqual(client_dict["city"], self.sample_data["city"])
        self.assertEqual(client_dict["phone_number"], self.sample_data["phone_number"])

    def test_from_dict(self):
        client = ClientRecord.from_dict(self.sample_data)
        self.assertEqual(client.name, self.sample_data["name"])
        self.assertEqual(client.city, self.sample_data["city"])
        self.assertEqual(client.phone_number, self.sample_data["phone_number"])

    def test_validation_success(self):
        errors = ClientRecord.validate(self.sample_data)
        self.assertEqual(errors, {})

    def test_validation_missing_required_fields(self):
        invalid_data = self.sample_data.copy()
        del invalid_data["name"]
        errors = ClientRecord.validate(invalid_data)
        self.assertIn("name", errors)

    def test_validation_invalid_phone_number(self):
        invalid_data = self.sample_data.copy()
        invalid_data["phone_number"] = "invalid-phone"
        errors = ClientRecord.validate(invalid_data)
        self.assertIn("phone_number", errors)

if __name__ == "__main__":
    unittest.main()
