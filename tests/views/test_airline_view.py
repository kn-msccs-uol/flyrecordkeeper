import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import unittest
import tkinter as tk
from views.airline_view import AirlineView

class DummyAirline:
    def __init__(self, id, company_name):
        self.id = id
        self.company_name = company_name
        self.type = "airline"

class DummyRecordManager:
    def __init__(self):
        self.airlines = [
            DummyAirline(1, "SkyHigh"),
            DummyAirline(2, "CloudFly")
        ]
    def get_records_by_type(self, record_type):
        return self.airlines
    def get_record_by_id(self, record_id, record_type):
        for airline in self.airlines:
            if airline.id == record_id:
                return airline
    def create_airline(self, name):
        return DummyAirline(3, name)
    def delete_record(self, record_id, record_type):
        self.airlines = [a for a in self.airlines if a.id != record_id]
        return True
    def save_to_file(self):
        pass

class TestAirlineView(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.rec_man = DummyRecordManager()
        self.view = AirlineView(self.root, self.rec_man)
        self.view.refresh_treeview()

    def tearDown(self):
        self.view.destroy()
        self.root.destroy()

    def test_treeview_populated(self):
        children = self.view.treeview.get_children()
        self.assertEqual(len(children), 2)

    def test_search_item_found(self):
        self.view.search_var.set("SkyHigh")
        self.view.search_item()
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
