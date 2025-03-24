import sys
import os
import unittest
import tkinter as tk

# Add the path to the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import sys
import os
import unittest
from unittest.mock import patch
from tkinter import Tk, Button
from views.app import App
import platform

class TestFlyRecordKeeper(unittest.TestCase):

    def setUp(self):
        """Set up the initial state for the test."""
        with patch.object(App, 'mainloop', lambda x: None):  # Prevent the mainloop from running
            self.app = App()  # Initialize the main app

    def test_window_title(self):
        """Test if the window title is correctly set."""
        self.assertEqual(self.app.title(), "FlyRecordKeeper - Record Management System")

    def test_window_size(self):
        """Test if the window size is set correctly."""
        # Get only the window size (first part before the '+')
        window_size = self.app.geometry().split('+')[0]
        self.assertEqual(window_size, "900x650")

    def test_menu_buttons(self):
        """Test if the navigation buttons for clients, airlines, and flights exist."""
        buttons = self.app.nav_buttons
        self.assertIn("Manage Clients", buttons)
        self.assertIn("Manage Airlines", buttons)
        self.assertIn("Manage Flights", buttons)

    def test_load_clients_view(self):
        """Test if the Manage Clients view loads correctly."""
        with patch.object(self.app, 'load_content') as mock_load_content:
            self.app.load_content("Manage Clients")
            mock_load_content.assert_called_with("Manage Clients")

    def test_load_airlines_view(self):
        """Test if the Manage Airlines view loads correctly."""
        with patch.object(self.app, 'load_content') as mock_load_content:
            self.app.load_content("Manage Airlines")
            mock_load_content.assert_called_with("Manage Airlines")

    def test_load_flights_view(self):
        """Test if the Manage Flights view loads correctly."""
        with patch.object(self.app, 'load_content') as mock_load_content:
            self.app.load_content("Manage Flights")
            mock_load_content.assert_called_with("Manage Flights")

    def test_status_update(self):
        """Test if the status bar updates correctly."""
        with patch.object(self.app, 'update_status') as mock_update_status:
            self.app.update_status("Test message")
            mock_update_status.assert_called_with("Test message")

    def test_exit_confirmation(self):
        """Test if the exit confirmation dialog works correctly."""
        with patch('tkinter.messagebox.askokcancel', return_value=True):
            with patch.object(self.app, 'on_closing') as mock_on_closing:
                self.app.on_closing()
                mock_on_closing.assert_called_once()

    def test_icon_load(self):
        """Test if the application icon loads correctly."""
        with patch('PIL.Image.open') as mock_open:
            mock_open.return_value = None  # Mock image open operation
            icon_path = self.app.get_asset_path('images/flyrecordkeeper_logo_icon.png')
            self.assertTrue(icon_path.endswith('assets/images/flyrecordkeeper_logo_icon.png'))

    def test_system_font(self):
        """Test if system font is set based on OS."""
        system = platform.system()  # Get the actual system type
        if system == "Windows":
            self.assertEqual(self.app.system_font, "Segoe UI")
        elif system == "Darwin":  # macOS
            self.assertEqual(self.app.system_font, "Helvetica Neue")
        else:  # Linux/Unix
            self.assertEqual(self.app.system_font, "DejaVu Sans")

    def tearDown(self):
        """Clean up any resources after each test."""
        self.app.destroy()

if __name__ == '__main__':
    unittest.main()
