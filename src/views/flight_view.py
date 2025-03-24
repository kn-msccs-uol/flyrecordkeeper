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

    def __init__(self, parent, update_status=None):
        super(FlightView, self).__init__()

        self.parent = parent

        # Store the update_status function
        self.update_status = update_status or (lambda msg: None)

        # Detect and configure system fonts
        import platform
        import tkinter.font as tkfont

        system = platform.system()
        self.default_font = tkfont.nametofont("TkDefaultFont")

        if system == "Windows":
            system_font = "Segoe UI"
            self.button_font = ("Segoe UI Emoji", 11)
        elif system == "Darwin":  # macOS
            system_font = "Helvetica Neue"
            self.button_font = ("Apple Color Emoji", 11)
        else:  # Linux/Unix
            system_font = "DejaVu Sans"
            self.button_font = ("Noto Color Emoji", 11)

        self.default_font.configure(family=system_font, size=10)

        # Configure bold font
        self.bold_font = tkfont.Font(font=self.default_font)
        self.bold_font.configure(weight="bold", size=14)

        self.rec_man = record_manager.RecordManager()

        self.setup_button_styles
        self.create_toolbar()
        self.create_treeview()

    def setup_button_styles(self):
        style = ttk.Style()
        style.configure('Add.TButton', font=self.button_font, width=10)
        style.configure('Edit.TButton', font=self.button_font, width=15)
        style.configure('Delete.TButton', font=self.button_font, width=10)
        style.configure('Search.TButton', font=self.button_font, width=10)

    def create_toolbar(self):
        """Create the toolbar with Add and Search buttons."""
        toolbar = ttk.Frame(self.parent)
        toolbar.pack(fill=tk.X)

        label = ttk.Label(toolbar, text="Flight Records", font=self.bold_font)
        label.pack(pady=5)

        # Add a separator
        separator = ttk.Separator(toolbar, orient='horizontal')
        separator.pack(fill='x', pady=(10,0))

        self.add_button = ttk.Button(toolbar, text="➕ Add", style='Add.TButton', command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = ttk.Button(toolbar, text="✏️ Edit/Update", style='Edit.TButton', command=self.edit_item, state="disabled")
        self.edit_button.pack(side=tk.LEFT, padx=15, pady=5)

        self.delete_button = ttk.Button(toolbar, text="❌ Delete", style='Delete.TButton', command=self.delete_item, state="disabled")
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Search implementation
        self.search_frame = ttk.Frame(toolbar)
        self.search_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create search variable and entry widget
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame, 
            textvariable=self.search_var,
            font=(self.default_font, 11),
            width=20
        )

        # Bind events to the entry widget
        self.search_entry.bind("<Return>", lambda e: self.perform_search())
        self.search_entry.bind("<Escape>", lambda e: self.toggle_search_mode())
        self.search_entry.bind("<FocusOut>", self.handle_focus_out)

        # Create a button with a magnifying glass icon
        self.search_button = ttk.Button(
            self.search_frame,
            text="🔍 Search",
            style='Search.TButton',
            command=self.toggle_search_mode
        )

        # Initially show the button
        self.search_button.pack(side=tk.RIGHT)

        # Track the current search mode
        self.is_search_mode = False

    def create_treeview(self):
        # Define a style for the Treeview
        #style = ttk.Style()
        #style.configure('Treeview', font=(12))
        # Configure the font for Treeview items
        #style.configure('Treeview.Heading', font=(12, 'bold'))
                        
        """Create the treeview widget to display data."""
        treeview_frame = tk.Frame(self.parent)
        treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Create a horizontal scrollbar
        self.h_scrollbar = ttk.Scrollbar(treeview_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create the treeview widget
        self.treeview = ttk.Treeview(
            treeview_frame,
            columns=("id", "client", "airline", "dateTime", "start_city", "end_city"),
            show="headings",
            xscrollcommand=self.h_scrollbar.set
        )

        # Configure scrollbar to work with treeview
        self.h_scrollbar.config(command=self.treeview.xview)

        # Define column headers and base widths
        self.column_base_widths = {
            "id": 70,                # Fixed width for ID
            "client": 150,           # Reasonable space for names
            "airline": 150,
            "dateTime": 200,         # Date/Time
            "start_city": 120,       # Most city names fit in this width
            "end_city": 120,
        }

        # Configure all columns with headings and widths
        for col, width in self.column_base_widths.items():
            display_name = col.replace("_", " ").title()
            if col == "id":
                display_name = "ID"
            elif col == "dateTime":
                display_name = "Date/Time"

            # All columns should respect their base width initially
            self.treeview.heading(col, text=display_name)
            self.treeview.column(col, width=width, minwidth=width//2, stretch=True)

        # Load data
        data = self.rec_man.get_records_by_type('flight')
        for item in data:
            self.display_rec(item, "insert")
            #self.treeview.insert("", "end", values=(
            #    item.id, item.client_id, item.airline_id, item.date,
            #   item.start_city, item.end_city
            #    ))

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

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete 'Flight ID: {row_id}'?"):
            try:
                if not item_data or len(item_data['values']) == 0:
                    return

                if (self.rec_man.delete_record(row_id, "flight")):
                    self.treeview.delete(self.selected_item)
                    messagebox.showinfo("Delete Successful", "Flight deleted successfully!")
                    self.update_status(f"'Flight ID: {row_id}' has been successfully deleted")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.update_status(f"Error deleting flight: {str(e)}")

    def search_item(self):
        """
        Handle searching for flights based on the search query.
        
        Supports searching by:
        - All fields (partial or full match)
        - Multiple criteria (separated by spaces or commas)
        """
        # Get the search query from the search variable
        search_query = self.search_var.get().strip()
        
        # If no query entered but search was triggered, show all records
        if not search_query:
            self.refresh_treeview()
            return
        
        # Use the SearchController to search for flights
        from controllers.search_controller import SearchController
        search_controller = SearchController(self.rec_man)
        search_results = search_controller.search_flights(search_query)
        
        # Update the treeview with the results
        self.update_treeview_with_results(search_results)

    def update_treeview_with_results(self, search_results):
        """
        Update the treeview with the returned flight records.
        
        Args:
            search_results: List of flight records to display
        """
        # Clear the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Populate the treeview with the filtered results
        for flight in search_results:
            self.display_rec(flight, "insert")

    def refresh_treeview(self):
        """Refresh the treeview with all flight records."""
        all_flights = self.rec_man.get_records_by_type('flight')
        self.update_treeview_with_results(all_flights)

    def toggle_search_mode(self):
        """Toggle between search button and search entry field."""
        if not self.is_search_mode:
            # Switch to search entry mode
            self.search_button.pack_forget()
            self.search_entry.pack(side=tk.RIGHT, fill=tk.X)
            self.search_entry.focus_set()  # Set focus to the entry field
            self.is_search_mode = True
        else:
            # Switch back to button mode
            self.search_entry.pack_forget()
            self.search_button.pack(side=tk.RIGHT)
            self.is_search_mode = False

    def perform_search(self):
        """Execute the search and revert to button mode."""
        # Call the original search method
        self.search_item()
        
        # Toggle back to button mode
        if self.is_search_mode:
            self.toggle_search_mode()

    def handle_focus_out(self, event):
        """Handle the focus out event with a small delay to allow clicks to register."""
        if self.is_search_mode:
            # Schedule the toggle after a short delay (75ms)
            # This delay prevents interference with click events
            self.master.after(75, self.toggle_search_mode)

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
        # Store original name if editing
        if action == "Edit":
            original_client_id = rec.client_id
            original_airline_id = rec.airline_id
            original_date = rec.date
            original_start_city = rec.start_city
            original_end_city = rec.end_city

        rec = self.resolve_references(rec)
        result, output = flight_capture.FlightCapture(self.rec_man, rec, action).show()

        if (result):
            if (action == "Add"):
                self.rec_man.flights.append(output)
                self.display_rec(output, "insert")

                self.update_status(f"New flight (ID: {output.id}) has been successfully added")
            elif (action == "Edit"):
                for a in self.rec_man.flights:
                    if a.id == output.id:
                        a.client_id = output.client_id
                        a.airline_id = output.airline_id
                        a.date = output.date
                        a.start_city = output.start_city
                        a.end_city = output.end_city
                        self.display_rec(output, "update")

                        # Check which fields have changed
                        original_values = [
                            original_client_id, original_airline_id, original_airline_id, 
                            original_date, original_start_city, original_end_city
                        ]
                        new_values = [
                            output.client_id, output.airline_id, output.airline_id, 
                            output.date, output.start_city, output.end_city
                            ]
                        
                        # Get a list of changed fields
                        changed_fields = [i for i, (orig, new) in enumerate(zip(original_values, new_values)) if orig != new]

                        if not changed_fields:
                            # No fields were changed, no status update
                            pass

                        else:
                            self.update_status(f"'Flight ID: {output.id}' has been successfully updated")

        self.rec_man.save_to_file()
