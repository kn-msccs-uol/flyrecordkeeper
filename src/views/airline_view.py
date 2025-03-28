import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from views import airline_capture

class AirlineView(ttk.Frame):
    parent = None
    rec_man = None
    selected_item = None

    def __init__(self, parent, rec_man, update_status=None):
        super(AirlineView, self).__init__()

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

        self.rec_man = rec_man

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

        label = ttk.Label(toolbar, text="Airline Company Records", font=self.bold_font)
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
        treeview_frame = ttk.Frame(self.parent)
        treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Create the treeview widget
        self.treeview = ttk.Treeview(
             treeview_frame,
             columns=("id",
                      "company_name"),
                      show="headings")

        # Define column headers and base widths
        self.column_base_widths = {
            "id": 70,                # Fixed width for ID
        }

        # Configure ID column with heading and width
        self.treeview.heading("id", text="ID")
        self.treeview.column("id", width=70, minwidth=70//2, stretch=False)

        # Configure company_name column to be dynamic
        self.treeview.heading("company_name", text="Company Name")
        self.treeview.column("company_name", stretch=True)

        # Load data
        data = self.rec_man.get_records_by_type('airline')
        for item in data:
            self.treeview.insert("", "end", values=(item.id, item.company_name))

        # Pack the treeview
        self.treeview.pack(expand=True, fill=tk.BOTH)
        self.treeview.bind('<<TreeviewSelect>>', self.select_item)

        # Bind to Configure event for handling resize
        self.treeview.bind("<Configure>", self.on_treeview_configure)

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

        # fixed: ID; proportionally variable: compnay name)
        id_width = self.column_base_widths["id"]
        available_width = treeview_width - id_width

        # Set ID column fixed
        self.treeview.column("id", width=id_width, stretch=False)

        # Distribute remaining width proportionally
        self.treeview.column("company_name", width=available_width, stretch=True)
        
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
        rec = self.rec_man.create_airline("")

        self.open_child_window(rec, "Add")

    def edit_item(self):
        """Handle editing an item by opening a child window."""
        if (self.selected_item is None):
            return
        
        item_data = self.treeview.item(self.selected_item)

        if not item_data or len(item_data['values']) == 0:
            return

        row_id = int(item_data['values'][0])
        rec = self.rec_man.get_record_by_id(row_id, "airline")
        self.open_child_window(rec, "Edit")

    def delete_item(self):
        """Handle deleting an item through a confirmation box."""
        if (self.selected_item is None):
            messagebox.showinfo("Info", "Please select an airline to delete")
            return
        
        item_data = self.treeview.item(self.selected_item)
        row_id = int(item_data['values'][0])
        record_name = str(item_data['values'][1])

        # Truncate long names to prevent status bar overflow
        old_display = self.truncate_name(record_name)

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete airline '{old_display}'?"):
            try:
                if not item_data or len(item_data['values']) == 0:
                    return

                if (self.rec_man.delete_record(row_id, "airline")):
                    self.treeview.delete(self.selected_item)
                    messagebox.showinfo("Delete Successful", "Airline deleted successfully!")
                    self.update_status(f"Airline '{old_display}' (ID: {row_id}) has been successfully deleted")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.update_status(f"Error deleting airline: {str(e)}")
    
    def truncate_name(self, name, max_length=30):
        """Truncate a string if it exceeds the maximum length."""
        return (name[:max_length] + "...") if len(name) > max_length else name

    def search_item(self):
        """
        Handle searching for airlines based on the search query.
        
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
        
        # Use the SearchController to search for airlines
        from controllers.search_controller import SearchController
        search_controller = SearchController(self.rec_man)
        search_results = search_controller.search_airlines(search_query)
        
        # Update the treeview with the results
        self.update_treeview_with_results(search_results)

    def update_treeview_with_results(self, search_results):
        """
        Update the treeview with the returned airline records.
        
        Args:
            search_results: List of airline records to display
        """
        # Clear the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Populate the treeview with the filtered results
        for airline in search_results:
            self.treeview.insert("", "end", values=(airline.id, airline.company_name))

    def refresh_treeview(self):
        """Refresh the treeview with all airline records."""
        all_airlines = self.rec_man.get_records_by_type('airline')
        self.update_treeview_with_results(all_airlines)

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
            original_name = rec.company_name
        
        result, output = airline_capture.AirlineCapture(rec, action).show()

        if (result):
            if (action == "Add"):
                self.rec_man.airlines.append(output)
                self.treeview.insert("", "end", values=(output.id, output.company_name))

                # Truncate long names to prevent status bar overflow
                new_display = self.truncate_name(output.company_name)

                self.update_status(f"New airline '{new_display}' (ID: {output.id}) has been successfully added")
            elif (action == "Edit"):
                for a in self.rec_man.airlines:
                    if a.id == output.id:
                        a.company_name = output.company_name
                        self.treeview.item(self.selected_item, text="", values=(output.id, output.company_name))

                        # Truncate long names to prevent status bar overflow
                        old_display = self.truncate_name(original_name)
                        new_display = self.truncate_name(output.company_name)

                        if output.company_name != original_name:
                            self.update_status(f"Airline (ID: {output.id}) successfully updated: '{old_display}' ⟶ '{new_display}'")

        self.rec_man.save_to_file()
