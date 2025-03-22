import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from models.client_record import ClientRecord

class TestClientRecord(unittest.TestCase):

    def setUp(self):
        # Sample valid client data
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
        # Create a ClientRecord object using the valid data
        self.client = ClientRecord.from_dict(self.valid_data)

    def test_initialization(self):
        # Check if values are stored correctly in the object
        self.assertEqual(self.client.id, 1)
        self.assertEqual(self.client.name, "John Doe")
        self.assertEqual(self.client.city, "London")
        self.assertEqual(self.client.type, "client")

    def test_to_dict(self):
        # Check if converting the object to dictionary gives the same data
        self.assertEqual(self.client.to_dict(), self.valid_data)

    def test_from_dict(self):
        # Check if we can create a ClientRecord from a dictionary
        client = ClientRecord.from_dict(self.valid_data)
        self.assertIsInstance(client, ClientRecord)
        self.assertEqual(client.name, "John Doe")

    def test_validate_valid_data(self):
        # This will call the real validation function and check for no errors
        errors = ClientRecord.validate(self.valid_data)
        self.assertEqual(errors, {})  # Expect no errors

    def test_validate_missing_name(self):
        # Create a copy of valid data with name removed
        invalid_data = self.valid_data.copy()
        del invalid_data["name"]

        # Run validation
        errors = ClientRecord.validate(invalid_data)

        # Check that "name" is in the error messages
        self.assertIn("name", errors)

if __name__ == "__main__":
    unittest.main()
