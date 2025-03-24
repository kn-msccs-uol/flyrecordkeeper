import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
import tkinter as tk
from unittest.mock import MagicMock
from tkinter import ttk
from views.airline_capture import AirlineCapture

    #Mock for record class
class MockRecord:
       def __init__(self, record_id, company_name):
        self.id = record_id
        self.company_name = company_name

    #Set up of sample data
        
class TestAirlineCapture(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.sample_data = MockRecord(1,"British Airways")
        self.capture = AirlineCapture(self.sample_data)

    #Test initialisation stage
    def test_initialise(self):
        self.assertEqual(self.capture.rec.id, 1)
        self.assertEqual(self.capture.rec.company_name, "British Airways")
        self.assertEqual(self.capture.action, "Add")
        self.assertFalse(self.capture.result)

    #Test updating action
    def test_update_rec(self):
        update_company_name = "Updated Airline"
        self.capture.name_entry.delete(0, tk.END)
        self.capture.name_entry.insert(0, update_company_name)
        self.capture.update_rec()
        self.assertEqual(self.capture.rec.company_name, update_company_name)   
        
    #Test validation of sample data
    def test_validation_success(self):
        self.capture.name_entry.delete(0, tk.END)
        self.capture.name_entry.insert(0, "Valid Airline")
        self.assertTrue(self.capture.validate())

    def test_validation_missing_name(self):
        self.capture.name_entry.delete(0, tk.END)
        self.assertFalse(self.capture.validate())

    def test_validation_short_name(self):
        short_name = "A"
        self.capture.name_entry.delete(0, tk.END)
        self.capture.name_entry.insert(0, short_name)
        self.assertFalse(self.capture.validate())

    #Test functionality 'ok' button
    def test_ok_action(self):
        self.capture.name_entry.delete(0, tk.END)
        self.capture.name_entry.insert(0, "New Airline")
        self.capture.ok()
        self.assertTrue(self.capture.result)

        self.assertEqual(self.capture.rec.company_name, "New Airline")

    #Test functionality 'cancel' button
    def test_cancel_action(self):
        self.capture.cancel()
        self.assertFalse(self.capture.result) 


if __name__ == "__main__":
    unittest.main()
