import sys
import os
import unittest
import tkinter as tk

# Add the path to the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from views.app import App

class TestAppBasicInitialization(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent main root window from showing

    def test_app_minimal_init(self):
        # Create the App instance without running full __init__
        app = App.__new__(App)
        tk.Tk.__init__(app)

        app.title("Test App Title")
        self.assertEqual(app.title(), "Test App Title")

        app.geometry("800x600")
        app.update_idletasks()  # Force geometry update

        width = app.winfo_width()
        height = app.winfo_height()

        self.assertEqual(width, 800)
        self.assertEqual(height, 600)

        app.destroy()

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
