import tkinter as tk
from tkinter import ttk, messagebox


class AirlineCapture(tk.Toplevel):
    def __init__(self, rec, action="Add"):
        super().__init__()
        
        # Set window properties
        self.title(f"{action} Airline Company Name")
        self.geometry("420x200")
        self.resizable(False, False)
        
        # Make it modal
        self.transient()
        self.grab_set()
        
        # Store the record and initialize result
        self.rec = rec
        self.result = False
        self.action = action
        
        # Create interface
        self.setup_interface()
        
        # Bind data
        self.bind_rec()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_interface(self):
        """Set up the interface elements."""
        # Main content frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame, padding=(15, 10))
        header_frame.pack(fill=tk.X)
        
        header_label = ttk.Label(
            header_frame, 
            text=f"{self.action} Airline", 
            font=('Segoe UI', 11, 'bold')
        )
        header_label.pack(anchor=tk.W)
        
        # Separator after header
        sep = ttk.Separator(main_frame, orient='horizontal')
        sep.pack(fill='x')
        
        # Content frame with padding
        content_frame = ttk.Frame(main_frame, padding=(20, 15))
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # ID field (display only)
        id_label = ttk.Label(content_frame, text="ID:", width=15, anchor="w")
        id_label.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="w")
        
        self.id_value = ttk.Label(content_frame, text=self.rec.id, width=25, anchor="w")
        self.id_value.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="w")
        
        # Company Name field (editable)
        name_label = ttk.Label(content_frame, text="Company Name:", width=15, anchor="w")
        name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.name_entry = ttk.Entry(content_frame, width=30)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        
        # Button toolbar
        button_frame = ttk.Frame(main_frame, padding=(10, 10))
        button_frame.pack(fill=tk.X)
        
        # OK and Cancel buttons
        cancel_button = tk.Button(button_frame, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        ok_button = tk.Button(button_frame, text="OK", width=10, command=self.ok)
        ok_button.pack(side=tk.RIGHT, padx=5)
    
    def bind_rec(self):
        """Bind record data to the interface elements."""
        self.name_entry.insert(0, self.rec.company_name)
        
        # Set focus to the name field for immediate editing
        self.name_entry.focus_set()
    
    def validate(self):
        """Validate the input data before accepting it."""
        company_name = self.name_entry.get().strip()
        
        if not company_name:
            messagebox.showerror("Validation Error", "Company Name cannot be empty.")
            self.name_entry.focus_set()
            return False
        
        if len(company_name) > 100:
            messagebox.showerror("Validation Error", "Company Name cannot exceed 100 characters.")
            self.name_entry.focus_set()
            return False
        
        return True
    
    def update_rec(self):
        """Update the record with values from the interface."""
        self.rec.company_name = self.name_entry.get().strip()
    
    def cancel(self):
        """Handle the Cancel button action."""
        self.result = False
        self.destroy()
    
    def ok(self):
        """Handle the OK button action."""
        if self.validate():
            self.update_rec()
            self.result = True
            # Close the child window after the action
            self.destroy()
    
    def show(self):
        """
        Display the dialog and wait for user interaction.
        
        Returns:
            Tuple containing (result, record) where result is True if OK was clicked
        """
        self.wm_deiconify()
        self.name_entry.focus_force()
        self.wait_window()
        return (self.result, self.rec)
