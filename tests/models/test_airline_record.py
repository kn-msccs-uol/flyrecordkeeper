import unittest
from models.airline_record import AirlineRecord

class TestAirlineRecord(unittest.TestCase):

    def setUp(self):
        """Set up a test instance of AirlineRecord"""
        self.record_id = 1
        self.company_name = "FlyHigh Airlines"
        self.airline_record = AirlineRecord(self.record_id, self.company_name)

    def test_initialization(self):
        """Test that an AirlineRecord instance initializes correctly"""
        self.assertEqual(self.airline_record.record_id, self.record_id)
        self.assertEqual(self.airline_record.company_name, self.company_name)
        self.assertEqual(self.airline_record.record_type, "airline")

    def test_to_dict(self):
        """Test the to_dict method for correct serialization"""
        expected_dict = {
            "id": self.record_id,
            "record_type": "airline",
            "company_name": self.company_name
        }
        self.assertEqual(self.airline_record.to_dict(), expected_dict)

    def test_from_dict(self):
        """Test the from_dict method for correct deserialization"""
        data = {
            "id": self.record_id,
            "company_name": self.company_name
        }
        new_airline_record = AirlineRecord.from_dict(data)

        self.assertEqual(new_airline_record.record_id, self.record_id)
        self.assertEqual(new_airline_record.company_name, self.company_name)
        self.assertEqual(new_airline_record.record_type, "airline")

    def test_inheritance(self):
        """Ensure AirlineRecord inherits from BaseRecord"""
        self.assertTrue(hasattr(self.airline_record, "record_type"))
        self.assertEqual(self.airline_record.record_type, "airline")

if __name__ == "__main__":
    unittest.main()



