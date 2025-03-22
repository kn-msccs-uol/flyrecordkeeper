import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from models.client_record import ClientRecord
from unittest.mock import patch

class TestClientRecord(unittest.TestCase):

    def setUp(self):
        self.valid_data = {
            "id": 1,
            "type": "client",
            "name": "John Doe",
            "address_line1": "123 Street",
            "address_line2": "Suite 200",
            "address_line3": "",
            "city": "London",
            "state": "Greater London",
            "zip_code": "SW1A 1AA",
            "country": "UK",
            "phone_number": "+44 1234 567890"
        }
        self.client = ClientRecord.from_dict(self.valid_data)

    def test_initialization(self):
        self.assertEqual(self.client.id, 1)
        self.assertEqual(self.client.name, "John Doe")
        self.assertEqual(self.client.city, "London")
        self.assertEqual(self.client.type, "client")

    def test_to_dict(self):
        self.assertEqual(self.client.to_dict(), self.valid_data)

    def test_from_dict(self):
        client = ClientRecord.from_dict(self.valid_data)
        self.assertIsInstance(client, ClientRecord)
        self.assertEqual(client.name, self.valid_data["name"])

    @patch("utils.validators.validate_required_field", return_value=None)
    @patch("utils.validators.validate_string", return_value=None)
    @patch("utils.validators.validate_phone_number", return_value=None)
    def test_validate_valid_data(self, mock_phone, mock_string, mock_required):
        errors = ClientRecord.validate(self.valid_data)
        self.assertEqual(errors, {})

    @patch("utils.validators.validate_required_field", side_effect=lambda d, k: "Required" if k == "name" else None)
    def test_validate_missing_name(self, mock_required):
        data = self.valid_data.copy()
        del data["name"]
        errors = ClientRecord.validate(data)
        self.assertIn("name", errors)
        self.assertEqual(errors["name"], "Required")


if __name__ == "__main__":
    unittest.main()
