import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from views import flight_capture

class FlightView(tk.Frame):
    parent = None

    def __init__(self, parent):
        #super().__init__(self)
        super(FlightView, self).__init__()

        self.parent = parent

        self.create_toolbar()
        self.create_treeview()

    def create_toolbar(self):
        """Create the toolbar with Add and Search buttons."""
        toolbar = tk.Frame(self.parent)
        toolbar.pack(fill=tk.X)

        label = tk.Label(toolbar, text="Manage Flights")
        label.pack(pady=(5,10))

        add_button = tk.Button(toolbar, text="Add", width=10, command=self.add_item)
        add_button.pack(side=tk.LEFT, padx=5)

        add_button = tk.Button(toolbar, text="Edit", width=10, command=self.edit_item)
        add_button.pack(side=tk.LEFT, padx=5)

        add_button = tk.Button(toolbar, text="Delete", width=10, command=self.delete_item)
        add_button.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(toolbar, text="Search", width=10, command=self.search_item)
        search_button.pack(side=tk.LEFT, padx=5)

    def create_treeview(self):
        """Create the treeview widget to display data."""
        treeview_frame = tk.Frame(self.parent)
        treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Create the treeview widget
        treeview = ttk.Treeview(treeview_frame, columns=("Client", "Airline", "DateTime", "StartCity", "EndCity"), show="headings")
        
        # Define columns
        treeview.heading("Client", text="ID")
        treeview.heading("Airline", text="Airline")
        treeview.heading("DateTime", text="Date/Time")
        treeview.heading("StartCity", text="Start City")
        treeview.heading("EndCity", text="End City")

        # Insert some dummy data
        data = [
            ("Darryl", "Emirates", "2025/03/31", "Johannesburg", "Istanbul")
        ]
        for item in data:
            treeview.insert("", "end", values=item)

        treeview.pack(expand=True, fill=tk.BOTH)       

    def add_item(self):
        """Handle adding a new item by opening a child window."""
        self.open_child_window("Add Item")

    def edit_item(self):
        """Handle adding a new item by opening a child window."""
        self.open_child_window("Edit Item")

    def delete_item(self):
        """Handle adding a new item by opening a child window."""
        messagebox.askquestion("Delete", "Are You Sure?")

    def search_item(self):
        """Handle searching for an item by opening a child window."""
        self.open_child_window("Search Item")

    def open_child_window(self, action):
        """Open a modal child window with 'OK' and 'Cancel' buttons."""
        child_window = flight_capture.FlightCapture()
