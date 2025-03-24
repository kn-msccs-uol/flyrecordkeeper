import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models import record_manager

from views import client_capture

class ClientView(ttk.Frame):
    parent = None
    rec_man = None
    selected_item = None

    def __init__(self, parent, update_status=None):
        super(ClientView, self).__init__()

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

        label = ttk.Label(toolbar, text="Client Records", font=self.bold_font)
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
        """Create the treeview widget to display data."""
        # Define a style for the Treeview
        #style = ttk.Style()
        #style.configure('Treeview', font=(12))
        # Configure the font for Treeview items
        #style.configure('Treeview.Heading', font=(12, 'bold'))
        
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

        # Truncate long names to prevent status bar overflow
        old_display = self.truncate_name(record_name)

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete client '{old_display}'?"):
            try:
                if not item_data or len(item_data['values']) == 0:
                    return

                if (self.rec_man.delete_record(row_id, "client")):
                    self.treeview.delete(self.selected_item)
                    messagebox.showinfo("Delete Successful", "Client deleted successfully!")
                    self.update_status(f"Client '{old_display}' (ID: {row_id}) has been successfully deleted")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.update_status(f"Error deleting client: {str(e)}")

    def truncate_name(self, name, max_length=30):
        """Truncate a string if it exceeds the maximum length."""
        return (name[:max_length] + "...") if len(name) > max_length else name

    def search_item(self):
        """
        Handle searching for clients based on the search query.
        
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
        
        # Use the SearchController to search for clients
        from controllers.search_controller import SearchController
        search_controller = SearchController(self.rec_man)
        search_results = search_controller.search_clients(search_query)
        
        # Update the treeview with the results
        self.update_treeview_with_results(search_results)

    def update_treeview_with_results(self, search_results):
        """
        Update the treeview with the returned client records.
        
        Args:
            search_results: List of client records to display
        """
        # Clear the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Populate the treeview with the filtered results
        for client in search_results:
            self.treeview.insert("", "end", values=(client.id, client.name, client.address_line1,
                                                    client.address_line2, client.address_line3,
                                                    client.city, client.state, client.zip_code,
                                                    client.country, client.phone_number))

    def refresh_treeview(self):
        """Refresh the treeview with all client records."""
        all_clients = self.rec_man.get_records_by_type('client')
        self.update_treeview_with_results(all_clients)

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

    def open_child_window(self, rec, action):
        """Open a modal child window with 'OK' and 'Cancel' buttons."""
        # Store original name if editing
        original_name = None
        if action == "Edit":
            original_name = rec.name

        result, output = client_capture.ClientCapture(rec, action).show()

        if (result):
            if (action == "Add"):
                self.rec_man.clients.append(output)
                self.treeview.insert("", "end", values=(output.id, output.name, output.address_line1,
                                                        output.address_line2, output.address_line3, output.city,
                                                        output.state, output.zip_code, output.country, output.phone_number))
                
                # Truncate long names to prevent status bar overflow
                new_display = self.truncate_name(output.name)
                
                self.update_status(f"New client '{new_display}' (ID: {output.id}) has been successfully added")
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
                        
                        # Truncate long names to prevent status bar overflow
                        old_display = self.truncate_name(original_name)
                        new_display = self.truncate_name(output.name)

                        if old_display == new_display:
                            self.update_status(f"Client '{new_display}' (ID: {output.id}) has been successfully updated")
                        else:
                            self.update_status(f"Client (ID: {output.id})'s name has been successfully updated: '{old_display}' ⟶ '{new_display}'")

        self.rec_man.save_to_file()
