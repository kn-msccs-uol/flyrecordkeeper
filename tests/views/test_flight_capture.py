import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import unittest
from datetime import datetime, timedelta
import tkinter as tk

from views.flight_capture import FlightCapture

class DummyClient:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class DummyAirline:
    def __init__(self, id, company_name):
        self.id = id
        self.company_name = company_name

class DummyFlightRecord:
    def __init__(self):
        self.client_id = ""
        self.client_name = ""
        self.airline_id = ""
        self.airline_name = ""
        self.date = datetime.now() + timedelta(days=1)
        self.start_city = ""
        self.end_city = ""

class DummyRecordManager:
    def __init__(self):
        self.clients = [DummyClient("1", "Kevin")]
        self.airlines = [DummyAirline("A1", "SkyHigh")]

class TestFlightCapture(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window during test
        self.rec = DummyFlightRecord()
        self.rec_man = DummyRecordManager()

    def tearDown(self):
        self.root.update()
        self.root.destroy()

    def test_validate_all_fields_valid(self):
        window = FlightCapture(self.rec_man, self.rec)
        window.client_select.set("Kevin")
        window.airline_select.set("SkyHigh")
        window.txt_start_city.insert(0, "London")
        window.txt_end_city.insert(0, "Barcelona")
        window.txt_date.selection_set(datetime.now() + timedelta(days=1))

        valid = window.validate()
        self.assertTrue(valid)
        window.destroy()

    def test_validate_missing_client(self):
        window = FlightCapture(self.rec_man, self.rec)
        window.client_select.set("-- Please Select --")
        window.airline_select.set("SkyHigh")
        window.txt_start_city.insert(0, "London")
        window.txt_end_city.insert(0, "Barcelona")
        window.txt_date.selection_set(datetime.now() + timedelta(days=1))

        valid = window.validate()
        self.assertFalse(valid)
        window.destroy()

    def test_validate_past_date(self):
        window = FlightCapture(self.rec_man, self.rec)
        window.client_select.set("Kevin")
        window.airline_select.set("SkyHigh")
        window.txt_start_city.insert(0, "London")
        window.txt_end_city.insert(0, "Barcelona")
        window.txt_date.selection_set(datetime.now() - timedelta(days=1))

        valid = window.validate()
        self.assertFalse(valid)
        window.destroy()

if __name__ == '__main__':
    unittest.main()
