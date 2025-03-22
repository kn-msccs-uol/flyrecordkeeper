import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models import record_manager

from views import client_capture

class ClientView(ttk.Frame):
    parent = None
    rec_man = None
    selected_item = None

    def __init__(self, parent):
        super(ClientView, self).__init__()

        self.parent = parent
        self.rec_man = record_manager.RecordManager()

        self.create_toolbar()
        self.create_treeview()

    def create_toolbar(self):
        """Create the toolbar with Add and Search buttons."""
        toolbar = ttk.Frame(self.parent)
        toolbar.pack(fill=tk.X)

        label = ttk.Label(toolbar, text="Client Records", font=(12, 'bold'))
        label.pack(pady=5)

        # Add a separator
        separator = ttk.Separator(toolbar, orient='horizontal')
        separator.pack(fill='x', pady=(10,0))

        self.add_button = tk.Button(toolbar, text="Add", font=(12), width=10, command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(toolbar, text="Edit/Update", font=(12),  width=15, command=self.edit_item, state="disabled")
        self.edit_button.pack(side=tk.LEFT, padx=15, pady=5)

        self.delete_button = tk.Button(toolbar, text="Delete", font=(12),  width=10, command=self.delete_item, state="disabled")
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_button = tk.Button(toolbar, text="Search", font=(12), width=10, command=self.search_item)
        self.search_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_treeview(self):
        """Create the treeview widget to display data."""
        # Define a style for the Treeview
        style = ttk.Style()
        style.configure('Treeview', font=(12))
        # Configure the font for Treeview items
        style.configure('Treeview.Heading', font=(12, 'bold'))
        
        treeview_frame = ttk.Frame(self.parent)
        treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Create a horizontal scrollbar
        self.h_scrollbar = ttk.Scrollbar(treeview_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create the treeview widget
        self.treeview = ttk.Treeview(
            treeview_frame,
            columns=("id", "name", "address_line1", "address_line2", "address_line3",
                     "city", "state", "zip_code", "country", "phone_number"),
            show="headings",
            xscrollcommand=self.h_scrollbar.set
        )

        # Configure scrollbar to work with treeview
        self.h_scrollbar.config(command=self.treeview.xview)

        # Define column headers and base widths
        self.column_base_widths = {
            "id": 70,                # Fixed width for ID
            "name": 150,             # Reasonable space for names
            "address_line1": 200,    # Address lines need more space
            "address_line2": 200,
            "address_line3": 200,
            "city": 120,             # Most city names fit in this width
            "state": 100,            # State/province names
            "zip_code": 80,          # Postal/zip codes
            "country": 120,          # Country names
            "phone_number": 120      # Phone numbers with formatting
        }

        # Configure all columns with headings and widths
        for col, width in self.column_base_widths.items():
            display_name = col.replace("_", " ").title()
            if col == "id":
                display_name = "ID"

            # All columns should respect their base width initially
            self.treeview.heading(col, text=display_name)
            self.treeview.column(col, width=width, minwidth=width//2, stretch=True)

        # Load data
        data = self.rec_man.get_records_by_type('client')
        for item in data:
            self.treeview.insert("", "end", values=(
                item.id, item.name, item.address_line1, item.address_line2, 
                item.address_line3, item.city, item.state, item.zip_code, 
                item.country, item.phone_number
            ))

        # Pack the treeview
        self.treeview.pack(expand=True, fill=tk.BOTH)
        self.treeview.bind('<<TreeviewSelect>>', self.select_item)

        # Bind to Configure event for handling resize
        self.treeview.bind("<Configure>", self.on_treeview_configure)

        # Hide scrollbar initially (will be shown if needed)
        self.h_scrollbar.pack_forget()
        self._scrollbar_visible = False

        # Initial update after UI is stable
        self.treeview.after(500, self.adjust_columns_and_scrollbar)

    def on_treeview_configure(self, event=None):
        """Handle treeview configuration changes (like resize or moving to another screen)"""
        # Use after to avoid multiple rapid updates
        if hasattr(self, '_configure_after_id'):
            self.treeview.after_cancel(self._configure_after_id)
        self._configure_after_id = self.treeview.after(100, self.adjust_columns_and_scrollbar)

    def adjust_columns_and_scrollbar(self):
        """Adjust column widths proportionally and update scrollbar visibility"""
        # Safety check for destroyed widgets
        try:
            if not self.treeview.winfo_exists():
                return
        except:
            return  # Widget may have been destroyed
        
        # Get current treeview width
        treeview_width = self.treeview.winfo_width()
        if treeview_width <= 1:  # If treeview not yet rendered
            self.treeview.after(100, self.adjust_columns_and_scrollbar)
            return
        
        # Calculate total minimum width needed for all columns
        total_min_width = sum(self.column_base_widths.values())

        # Calculate if scrollbar is needed
        need_scrollbar = (total_min_width > treeview_width)

        if need_scrollbar:
            # Need scrollbar - use fixed minimum widths for all columns
            for col, width in self.column_base_widths.items():
                self.treeview.column(col, width=width, stretch=False)
            
            # Ensure scrollbar is visible
            if not self._scrollbar_visible:
                self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
                self._scrollbar_visible = True
        else:
            # No scrollbar needed (fixed: ID; proportionally variable: other columns)
            id_width = self.column_base_widths["id"]
            available_width = treeview_width - id_width

            # Get all columns except ID
            flex_columns = [col for col in self.treeview["columns"] if col != "id"]
            flex_total_base_width = sum(self.column_base_widths[col] for col in flex_columns)

            # Set ID column fixed
            self.treeview.column("id", width=id_width, stretch=False)

            # Distribute remaining width proportionally
            for col in flex_columns:
                proportion = self.column_base_widths[col] / flex_total_base_width
                new_width = max(self.column_base_widths[col], int(available_width * proportion))
                self.treeview.column(col, width=new_width, stretch=True)

            # Hide scrollbar
            if self._scrollbar_visible:
                self.h_scrollbar.pack_forget()
                self._scrollbar_visible = False
        
        # Update UI
        self.treeview.update_idletasks()

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
        rec = self.rec_man.create_client("")

        self.open_child_window(rec, "Add")

    def edit_item(self):
        """Handle editing an item by opening a child window."""
        if (self.selected_item is None):
            return
        
        item_data = self.treeview.item(self.selected_item)

        if not item_data or len(item_data['values']) == 0:
            return

        row_id = int(item_data['values'][0])
        rec = self.rec_man.get_record_by_id(row_id, "client")
        self.open_child_window(rec, "Edit")

    def delete_item(self):
        """Handle deleting an item through a confirmation box."""
        if (self.selected_item is None):
            messagebox.showinfo("Info", "Please select a client to delete")
            return
        
        item_data = self.treeview.item(self.selected_item)
        row_id = int(item_data['values'][0])
        record_name = str(item_data['values'][1])


        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete client '{record_name}'?"):
            try:
                if not item_data or len(item_data['values']) == 0:
                    return

                if (self.rec_man.delete_record(row_id, "client")):
                    self.treeview.delete(self.selected_item)
                    messagebox.showinfo("Delete Successful", "Client deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def search_item(self):
        """Handle searching for an item by opening a child window."""
        self.open_child_window(None, "Search")

    def open_child_window(self, rec, action):
        """Open a modal child window with 'OK' and 'Cancel' buttons."""
        result, output = client_capture.ClientCapture(rec, action).show()

        if (result):
            if (action == "Add"):
                self.rec_man.clients.append(output)
                self.treeview.insert("", "end", values=(output.id, output.name, output.address_line1,
                                                        output.address_line2, output.address_line3, output.city,
                                                        output.state, output.zip_code, output.country, output.phone_number))
            elif (action == "Edit"):
                for a in self.rec_man.clients:
                    if a.id == output.id:
                        a.name = output.name
                        a.address_line1 = output.address_line1
                        a.address_line2 = output.address_line2
                        a.address_line3 = output.address_line3
                        a.city = output.city
                        a.state = output.state
                        a.zip_code = output.zip_code
                        a.country = output.country
                        a.phone_number = output.phone_number
                        self.treeview.item(self.selected_item, text="", values=(output.id, output.name, output.address_line1,
                                                                                output.address_line2, output.address_line3, output.city,
                                                                                output.state, output.zip_code, output.country, output.phone_number))

        self.rec_man.save_to_file()
