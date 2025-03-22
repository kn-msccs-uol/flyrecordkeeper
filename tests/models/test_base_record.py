import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from models.base_record import BaseRecord

class TestBaseRecord(unittest.TestCase):

    def setUp(self):
        self.record_id = 101
        self.record_type = "airline"
        self.valid_data = {"id": self.record_id, "type": self.record_type}
        self.base_record = BaseRecord(self.record_id, self.record_type)

    def test_initialization(self):
        """Test that BaseRecord initializes with correct values"""
        self.assertEqual(self.base_record.id, self.record_id)
        self.assertEqual(self.base_record.type, self.record_type)

    def test_to_dict(self):
        """Test that to_dict() returns the correct dictionary"""
        expected = {"id": self.record_id, "type": self.record_type}
        self.assertEqual(self.base_record.to_dict(), expected)

    def test_from_dict(self):
        """Test creating BaseRecord from dictionary"""
        record = BaseRecord.from_dict(self.valid_data)
        self.assertIsInstance(record, BaseRecord)
        self.assertEqual(record.id, self.record_id)
        self.assertEqual(record.type, self.record_type)

    def test_validate_valid_data(self):
        """Test that validate() returns empty errors for valid data"""
        errors = BaseRecord.validate(self.valid_data)
        self.assertEqual(errors, {})

    def test_validate_invalid_id(self):
        """Test that validate() returns error for non-integer ID"""
        data = {"id": "abc", "type": "client"}
        errors = BaseRecord.validate(data)
        self.assertIn("id", errors)
        self.assertEqual(errors["id"], "ID must be an integer")

    def test_validate_invalid_type(self):
        """Test that validate() returns error for non-string type"""
        data = {"id": 1, "type": 123}
        errors = BaseRecord.validate(data)
        self.assertIn("type", errors)
        self.assertEqual(errors["type"], "Type must be a string")

    def test_validate_missing_fields(self):
        """Test that validate() ignores missing fields (optional fields)"""
        data = {}
        errors = BaseRecord.validate(data)
        self.assertEqual(errors, {})  # No error if keys are missing

if __name__ == '__main__':
    unittest.main()

