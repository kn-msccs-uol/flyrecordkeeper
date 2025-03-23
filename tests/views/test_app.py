import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from unittest.mock import MagicMock
import tkinter as tk
from tkinter import ttk
from views.app import App


#Test Tkinter Initialisation
class AppTest(unittest.Testcase):
    def test_init(self, mock_tk_init):
        mock_tk_init.return_value = None
        app = App()
        self.assertTrue(mock_tk_init.called)
        self.assertEqual(app.title(), "FlyRecordKeeper - Record Management System")
        self.assertEqual(app.geometry(), "900x650")

#Test Tkinter Layout Setup

    def test_setup_styles(self, mock_style):
        mock_style.return_value = MagicMock()
        app = App()
        app.setup_styles()
        self.assertTrue(mock_style().configure.called)

    def test_setup_layout(self, mock_frame):
        mock_frame.return_value = MagicMock()
        app = App()
        app.setup_layout()
        self.assertTrue(mock_frame.called)

#Test File Path Handling

    def test_get_asset_path(self, mock_sys, mock_path):
        mock_sys.frozen = False
        mock_path.dirname.return_value = "/mock/path"
        mock_path.join.return_value = "/mock/path/assets/test.png"

        app = App()
        asset_path = app.get_asset_path("test.png")
        self.assertEqual(asset_path, "/mock/path/assets/test.png")


#Test 'Exit' Button Functionality
    def test_on_closing(self, mock_askokcancel):
        mock_askokcancel.return_value = True
        app = App()
        with patch.object(app, "destroy") as mock_destroy:
            app.on_closing()
            self.assertTrue(mock_askokcancel.called)
            self.assertTrue(mock_destroy.called)
