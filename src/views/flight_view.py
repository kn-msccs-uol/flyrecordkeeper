import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime
from models import record_manager

from views import flight_capture

class FlightView(tk.Frame):
    parent = None
    rec_man = None
    selected_item = None

    def __init__(self, parent):
        super(FlightView, self).__init__()

        self.parent = parent
        self.rec_man = record_manager.RecordManager()

        self.create_toolbar()
        self.create_treeview()

    def create_toolbar(self):
        """Create the toolbar with Add and Search buttons."""
        toolbar = ttk.Frame(self.parent)
        toolbar.pack(fill=tk.X)

        label = ttk.Label(toolbar, text="Flight Records", font=(14,'bold'))
        label.pack(pady=5)

        # Add a separator
        separator = ttk.Separator(toolbar, orient='horizontal')
        separator.pack(fill='x', pady=(10,0))

        self.add_button = tk.Button(toolbar, text="Add", font=(12), width=10, command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(toolbar, text="Edit/Update", font=(12), width=15, command=self.edit_item, state="disabled")
        self.edit_button.pack(side=tk.LEFT, padx=15, pady=5)

        self.delete_button = tk.Button(toolbar, text="Delete", font=(12), width=10, command=self.delete_item, state="disabled")
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_button = tk.Button(toolbar, text="Search", font=(12), width=10, command=self.search_item)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_treeview(self):
        # Define a style for the Treeview
        style = ttk.Style()
        style.configure('Treeview', font=(12))
        # Configure the font for Treeview items
        style.configure('Treeview.Heading', font=(12, 'bold')
                        
        """Create the treeview widget to display data."""
        treeview_frame = tk.Frame(self.parent)
        treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Create the treeview widget
        self.treeview = ttk.Treeview(treeview_frame, columns=("ID", "Client", "Airline", "DateTime", "StartCity", "EndCity"), show="headings")
        
        # Define columns
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Client", text="Client")
        self.treeview.heading("Airline", text="Airline")
        self.treeview.heading("DateTime", text="Date/Time")
        self.treeview.heading("StartCity", text="Start City")
        self.treeview.heading("EndCity", text="End City")

        data = self.rec_man.get_records_by_type('flight')

        for item in data:
            self.display_rec(item, "insert")
            #self.treeview.insert("", "end", values=(item.id, item.client_id, item.airline_id, item.date, item.start_city, item.end_city))

        self.treeview.pack(expand=True, fill=tk.BOTH)

        self.treeview.bind('<ButtonRelease-1>', self.select_item)

    def select_item(self, a):
        """Selection change event on the treeview"""
        self.selected_item = self.treeview.focus()
        
        self.toggle_buttons(self.select_item is not None)

    def toggle_buttons(self, state):
        """Toggle Edit and Delete buttons based on selected item."""
        if (state):
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    def add_item(self):
        """Handle adding a new item by opening a child window."""
        rec = self.rec_man.create_flight(0, 0, datetime.now(), "", "")

        self.open_child_window(rec, "Add")

    def edit_item(self):
        """Handle adding a new item by opening a child window."""
        if (self.selected_item is None):
            return
        
        item_data = self.treeview.item(self.selected_item)

        if not item_data or len(item_data['values']) == 0:
            return

        row_id = int(item_data['values'][0])
        rec = self.rec_man.get_record_by_id(row_id, "flight")
        self.open_child_window(rec, "Edit")


    def delete_item(self):
        """Handle adding a new item by opening a child window."""
        if (self.selected_item is None):
            messagebox.showinfo("Info", "Please select a flight to delete")
            return
        
        item_data = self.treeview.item(self.selected_item)
        row_id = int(item_data['values'][0])
        record_name = str(item_data['values'][1])

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete airline '{record_name}'?"):
            try:
                if not item_data or len(item_data['values']) == 0:
                    return

                if (self.rec_man.delete_record(row_id, "flight")):
                    self.treeview.delete(self.selected_item)
                    messagebox.showinfo("Delete Successful", "Flight deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))


    def search_item(self):
        """Handle searching for an item by opening a child window."""
        self.open_child_window(None, "Search")

    def resolve_references(self, rec):
        """Resolve dependencies for name values."""
        if (int(rec.client_id) > 0):
            client_rec = self.rec_man.get_record_by_id(rec.client_id, "client")
            rec.client_name = client_rec.name or ""
        else:
            rec.client_name = ""

        if (int(rec.airline_id) > 0):
            airline_rec = self.rec_man.get_record_by_id(rec.airline_id, "airline")
            rec.airline_name = airline_rec.company_name or ""
        else:
            rec.airline_name = ""

        return rec

    def display_rec(self, rec, action):
        """Display the record on the grid after resolving dependencies for name values."""
        rec = self.resolve_references(rec)

        if (action == "update"):
            self.treeview.item(self.selected_item, text="", values=(rec.id, rec.client_name, rec.airline_name, rec.date, rec.start_city, rec.end_city))
        else:
            self.treeview.insert("", "end", values=(rec.id, rec.client_name, rec.airline_name, rec.date, rec.start_city, rec.end_city))

    def open_child_window(self, rec, action):
        """Open a modal child window with 'OK' and 'Cancel' buttons."""
        rec = self.resolve_references(rec)
        result, output = flight_capture.FlightCapture(self.rec_man, rec, action).show()

        if (result):
            if (action == "Add"):
                self.rec_man.flights.append(output)
                self.display_rec(output, "insert")
            elif (action == "Edit"):
                for a in self.rec_man.flights:
                    if a.id == output.id:
                        a.client_id = output.client_id
                        a.airline_id = output.airline_id
                        a.date = output.date
                        a.start_city = output.start_city
                        a.end_city = output.end_city
                        self.display_rec(output, "update")

        self.rec_man.save_to_file()
