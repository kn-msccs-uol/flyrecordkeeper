import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import unittest
import tkinter as tk
from views.client_view import ClientView

class DummyClient:
    def __init__(self, id, name, address_line1="", address_line2="", address_line3="", city="", state="", zip_code="", country="", phone_number=""):
        self.id = id
        self.name = name
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone_number = phone_number
        self.type = "client"

class DummyRecordManager:
    def __init__(self):
        self.clients = [
            DummyClient(1, "Kevin", city="London"),
            DummyClient(2, "Alice", city="Paris")
        ]
    def get_records_by_type(self, record_type):
        return self.clients
    def get_record_by_id(self, record_id, record_type):
        return next((c for c in self.clients if c.id == record_id), None)
    def create_client(self, name):
        return DummyClient(3, name)
    def delete_record(self, record_id, record_type):
        self.clients = [c for c in self.clients if c.id != record_id]
        return True
    def save_to_file(self):
        pass

class TestClientView(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.view = ClientView(self.root)
        self.view.rec_man = DummyRecordManager()
        self.view.refresh_treeview()

    def tearDown(self):
        self.view.destroy()
        self.root.destroy()

    def test_treeview_populated(self):
        children = self.view.treeview.get_children()
        self.assertEqual(len(children), 2)

    def test_search_item_found(self):
        self.view.search_var.set("Kevin")
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
