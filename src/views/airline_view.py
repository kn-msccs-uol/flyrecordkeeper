import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models import record_manager

from views import airline_capture

class AirlineView(tk.Frame):
    parent = None
    rec_man = None
    ctrl = None
    selected_item = None

    def __init__(self, parent):
        #super().__init__(self)
        super(AirlineView, self).__init__()

        self.parent = parent
        self.rec_man = record_manager.RecordManager()

        self.create_toolbar()
        self.create_treeview()

    def create_toolbar(self):
        """Create the toolbar with Add and Search buttons."""
        toolbar = tk.Frame(self.parent)
        toolbar.pack(fill=tk.X)

        label = tk.Label(toolbar, text="Manage Airlines")
        label.pack(pady=(5,10))

        self.add_button = tk.Button(toolbar, text="Add", width=10, command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(toolbar, text="Edit/Update", width=10, command=self.edit_item, state="disabled")
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(toolbar, text="Delete", width=10, command=self.delete_item, state="disabled")
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(toolbar, text="Search", width=10, command=self.search_item)
        self.search_button.pack(side=tk.RIGHT, padx=5)

    def create_treeview(self):
        """Create the treeview widget to display data."""
        treeview_frame = tk.Frame(self.parent)
        treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Create the treeview widget
        self.treeview = ttk.Treeview(treeview_frame, columns=("id", "company_name"), show="headings")
        
        # Define columns
        self.treeview.heading("id", text="ID")
        self.treeview.heading("company_name", text="Company Name")

        data = self.rec_man.get_records_by_type('airline')
        
        for item in data:
            self.treeview.insert("", "end", values=(item.id, item.company_name))

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
        rec = self.rec_man.create_airline("")

        self.open_child_window(rec, "Add")

    def edit_item(self):
        """Handle adding a new item by opening a child window."""
        if (self.selected_item is None):
            return
        
        item_data = self.treeview.item(self.selected_item)

        if not item_data or len(item_data['values']) == 0:
            return

        row_id = int(item_data['values'][0])
        rec = self.rec_man.get_record_by_id(row_id, "airline")
        self.open_child_window(rec, "Edit")

    def delete_item(self):
        """Handle adding a new item by opening a child window."""
        if (self.selected_item is None):
            messagebox.showinfo("Info", "Please select an airline to delete")
            return
        
        item_data = self.treeview.item(self.selected_item)
        row_id = int(item_data['values'][0])
        record_name = str(item_data['values'][1])


        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete airline '{record_name}'?")
        if confirm:
            try:
                if not item_data or len(item_data['values']) == 0:
                    return

                if (self.rec_man.delete_record(row_id, "airline")):
                    self.treeview.delete(self.selected_item)
                    messagebox.showinfo("Delete Successful", "Airline deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def search_item(self):
        """Handle searching for an item by opening a child window."""
        self.open_child_window(None, "Search")

    def open_child_window(self, rec, action):
        """Open a modal child window with 'OK' and 'Cancel' buttons."""
        result, output = airline_capture.AirlineCapture(rec).show()

        if (result):
            if (action == "Add"):
                self.rec_man.airlines.append(output)
                self.treeview.insert("", "end", values=(output.id, output.company_name))
            elif (action == "Edit"):
                for a in self.rec_man.airlines:
                    if a.id == output.id:
                        a.company_name = output.company_name
                        self.treeview.item(self.selected_item, text="", values=(output.id, output.company_name))

        self.rec_man.save_to_file()
