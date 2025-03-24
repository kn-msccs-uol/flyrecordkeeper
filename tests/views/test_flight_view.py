import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import unittest
import tkinter as tk
from datetime import datetime, timedelta
from views.flight_view import FlightView

class DummyClient:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class DummyAirline:
    def __init__(self, id, company_name):
        self.id = id
        self.company_name = company_name

class DummyFlight:
    def __init__(self, id, client_id, airline_id, date, start_city, end_city):
        self.id = id
        self.client_id = client_id
        self.airline_id = airline_id
        self.date = date
        self.start_city = start_city
        self.end_city = end_city
        self.client_name = ""
        self.airline_name = ""

class DummyRecordManager:
    def __init__(self):
        self.clients = [DummyClient(1, "Kevin")]
        self.airlines = [DummyAirline(1, "SkyHigh")]
        self.flights = [
            DummyFlight(1, 1, 1, datetime.now() + timedelta(days=1), "London", "Barcelona")
        ]

    def get_records_by_type(self, record_type):
        return self.flights if record_type == "flight" else []

    def get_record_by_id(self, record_id, record_type):
        if record_type == "client":
            return next((c for c in self.clients if c.id == record_id), None)
        elif record_type == "airline":
            return next((a for a in self.airlines if a.id == record_id), None)
        elif record_type == "flight":
            return next((f for f in self.flights if f.id == record_id), None)

    def create_flight(self, client_id, airline_id, date, start_city, end_city):
        return DummyFlight(2, client_id, airline_id, date, start_city, end_city)

    def delete_record(self, record_id, record_type):
        self.flights = [f for f in self.flights if f.id != record_id]
        return True

    def save_to_file(self):
        pass

class TestFlightView(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.rec_man = DummyRecordManager()
        self.view = FlightView(self.root, self.rec_man)
        self.view.refresh_treeview()

    def tearDown(self):
        self.view.destroy()
        self.root.destroy()

    def test_treeview_populated(self):
        children = self.view.treeview.get_children()
        self.assertEqual(len(children), 1)

    def test_toggle_search_mode(self):
        self.assertFalse(self.view.is_search_mode)
        self.view.toggle_search_mode()
        self.assertTrue(self.view.is_search_mode)
        self.view.toggle_search_mode()
        self.assertFalse(self.view.is_search_mode)

if __name__ == '__main__':
    unittest.main()
