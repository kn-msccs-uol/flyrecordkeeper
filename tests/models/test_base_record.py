import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from models.base_record import BaseRecord

class TestBaseRecord(unittest.TestCase):

    def setUp(self):
        """Set up a test instance of BaseRecord"""
        self.record_id = 101
        self.record_type = "airline"
        self.base_record = BaseRecord(self.record_id, self.record_type)

    def test_initialization(self):
        """Test that a BaseRecord instance initializes correctly"""
        self.assertEqual(self.base_record.id, self.record_id)
        self.assertEqual(self.base_record.type, self.record_type)

    def test_to_dict(self):
        """Test the to_dict method for correct serialization"""
        expected_dict = {
            "id": self.record_id,
            "type": self.record_type
        }
        self.assertEqual(self.base_record.to_dict(), expected_dict)

    def test_from_dict(self):
        """Test the from_dict method for correct deserialization"""
        data = {
            "id": self.record_id,
            "type": self.record_type
        }
        new_base_record = BaseRecord.from_dict(data)

        self.assertEqual(new_base_record.id, self.record_id)
        self.assertEqual(new_base_record.type, self.record_type)

    def test_record_type(self):
        """Ensure that record type is stored correctly"""
        self.assertTrue(hasattr(self.base_record, "type"))
        self.assertEqual(self.base_record.type, self.record_type)

if __name__ == "__main__":
    unittest.main()

