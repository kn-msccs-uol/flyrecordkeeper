import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from unittest.mock import MagicMock
from controllers.client_controller import ClientController
from models.record_manager import RecordManager

class TestClientController(unittest.TestCase):
    
    def setUp(self):
        self.mock_record_manager = MagicMock(spec=RecordManager)
        self.controller = ClientController(record_manager=self.mock_record_manager)
    
    def test_get_all_clients(self):
        self.mock_record_manager.get_records_by_type.return_value = [
            {"id": 1, "name": "Client A"},
            {"id": 2, "name": "Client B"}
        ]
        result = self.controller.get_all_clients()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Client A")
        self.mock_record_manager.get_records_by_type.assert_called_once_with("client")
    
    def test_get_client_found(self):
        self.mock_record_manager.get_record_by_id.return_value = {"id": 1, "type": "client", "name": "Client A"}
        result = self.controller.get_client(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Client A")
        self.mock_record_manager.get_record_by_id.assert_called_once_with(1)
    
    def test_get_client_not_found(self):
        self.mock_record_manager.get_record_by_id.return_value = None
        result = self.controller.get_client(999)
        self.assertIsNone(result)
    
    def test_create_client(self):
        self.mock_record_manager.create_record.return_value = {"id": 1, "name": "New Client"}
        result = self.controller.create_client("New Client", "Address 1", "Address 2", "Address 3", "City", "State", "Zip", "Country", "1234567890")
        self.assertEqual(result["name"], "New Client")
        self.mock_record_manager.create_record.assert_called_once()
    
    def test_update_client_success(self):
        self.mock_record_manager.get_record_by_id.return_value = {"id": 1, "type": "client", "name": "Old Client"}
        self.mock_record_manager.update_record.return_value = {"id": 1, "name": "Updated Client"}
        result = self.controller.update_client(1, name="Updated Client")
        self.assertEqual(result["name"], "Updated Client")
        self.mock_record_manager.update_record.assert_called_once()
    
    def test_update_client_not_found(self):
        self.mock_record_manager.get_record_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.controller.update_client(999, name="Updated Client")
        self.assertTrue("Client with ID 999 not found" in str(context.exception))
    
    def test_delete_client_success(self):
        self.mock_record_manager.get_record_by_id.return_value = {"id": 1, "type": "client", "name": "Client A"}
        self.mock_record_manager.delete_record.return_value = True
        result = self.controller.delete_client(1)
        self.assertTrue(result)
        self.mock_record_manager.delete_record.assert_called_once_with(1)
    
    def test_delete_client_not_found(self):
        self.mock_record_manager.get_record_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.controller.delete_client(999)
        self.assertTrue("Client with ID 999 not found" in str(context.exception))
    
    def test_search_clients(self):
        self.mock_record_manager.get_records_by_type.return_value = [
            {"id": 1, "name": "John Doe", "phone_number": "1234567890"},
            {"id": 2, "name": "Jane Smith", "phone_number": "0987654321"},
            {"id": 3, "name": "Alice Johnson", "phone_number": "1112223333"}
        ]
        result = self.controller.search_clients("John")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "John Doe")
        self.assertEqual(result[1]["name"], "Alice Johnson")

if __name__ == "__main__":
    unittest.main()

