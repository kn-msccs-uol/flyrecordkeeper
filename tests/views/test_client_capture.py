import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# Import built-in libraries
import unittest
import tkinter as tk
from unittest.mock import patch

# Import the ClientCapture window you're testing
from views.client_capture import ClientCapture

# Create a fake client record class to simulate real data
class MockClientRecord:
    def __init__(self, record_id, name="John Doe"):
        self.id = record_id
        self.name = name
        self.address_line1 = "123 Street"
        self.address_line2 = ""
        self.address_line3 = ""
        self.city = "London"
        self.state = "Greater London"
        self.zip_code = "E1 6AN"
        self.country = "UK"
        self.phone_number = "+441234567890"

# This is our test class
class TestClientCapture(unittest.TestCase):

    # This runs before every test
    def setUp(self):
        # Create a hidden Tkinter window (so the GUI doesn't pop up during testing)
        self.root = tk.Tk()
        self.root.withdraw()

        # Create a fake client record
        self.sample_data = MockClientRecord(1)

        # Open the form window with the mock data
        self.capture = ClientCapture(self.sample_data)

    # This runs after every test to clean up
    def tearDown(self):
        self.capture.destroy()
        self.root.destroy()

    # Check that the form loads correctly with the right values
    def test_initialise_fields(self):
        self.assertEqual(self.capture.rec.id, 1)
        self.assertEqual(self.capture.name_entry.get(), self.sample_data.name)
        self.assertEqual(self.capture.action, "Add")
        self.assertFalse(self.capture.result)

    # Check that updating the name field updates the record
    def test_update_rec(self):
        self.capture.name_entry.delete(0, tk.END)
        self.capture.name_entry.insert(0, "Jane Smith")
        self.capture.update_rec()
        self.assertEqual(self.capture.rec.name, "Jane Smith")

    # Check that validation passes with a good name
    @patch("tkinter.messagebox.showerror")  # This prevents the actual popup
    def test_validation_success(self, mock_error):
        self.capture.name_entry.delete(0, tk.END)
        self.capture.name_entry.insert(0, "Jane Smith")
        result = self.capture.validate()
        self.assertTrue(result)
        mock_error.assert_not_called()

    # Check that validation fails with a missing name
    @patch("tkinter.messagebox.showerror")
    def test_validation_missing_name(self, mock_error):
        self.capture.name_entry.delete(0, tk.END)
        result = self.capture.validate()
        self.assertFalse(result)
        mock_error.assert_called_once()

    # Check that clicking "Cancel" sets result to False
    def test_cancel_action(self):
        self.capture.cancel()
        self.assertFalse(self.capture.result)

    # Check that clicking "OK" with valid data saves and closes
    @patch("tkinter.messagebox.showerror")
    def test_ok_action_valid(self, mock_error):
        self.capture.name_entry.delete(0, tk.END)
        self.capture.name_entry.insert(0, "Valid Name")
        self.capture.ok()
        self.assertTrue(self.capture.result)
        self.assertEqual(self.capture.rec.name, "Valid Name")
        mock_error.assert_not_called()

    # Check that clicking "OK" with invalid data doesn’t save
    @patch("tkinter.messagebox.showerror")
    def test_ok_action_invalid(self, mock_error):
        self.capture.name_entry.delete(0, tk.END)
        self.capture.ok()
        self.assertFalse(self.capture.result)
        mock_error.assert_called_once()

# This runs the tests when you run the file
if __name__ == "__main__":
    unittest.main()
