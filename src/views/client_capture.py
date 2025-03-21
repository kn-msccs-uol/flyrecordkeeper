import tkinter as tk
from tkinter import ttk, messagebox

from utils.validators import validate_required_field, validate_string, validate_phone_number


class ClientCapture(tk.Toplevel):
    def __init__(self, rec, action="Add"):
        super().__init__()

        # Set window properties
        self.title(f"{action} Client Record")
        self.geometry("500x450")
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
            text=f"{self.action} Client", 
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

        # Configure grid layout
        content_frame.grid_columnconfigure(1, weight=1)

        # Name Field
        row = 1
        name_label = ttk.Label(content_frame, text="Name:", width=15, anchor="w")
        name_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        self.name_entry = ttk.Entry(content_frame, width=30)
        self.name_entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")

        # Address Fields
        address_fields = [
            ("Address Line 1:", "address_line1_entry"),
            ("Address Line 2:", "address_line2_entry"),
            ("Address Line 3:", "address_line3_entry")
        ]
        for label_text, attr_name in address_fields:
            row += 1
            label = ttk.Label(content_frame, text=label_text, width=15, anchor="w")
            label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(content_frame, width=40)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")
            setattr(self, attr_name, entry)

        # Location Fields
        location_fields = [
            ("City:", "city_entry", 20),
            ("State:", "state_entry", 20),
            ("Zip Code:", "zip_code_entry", 10),
            ("Country:", "country_entry", 20)
        ]
        for label_text, attr_name, width in location_fields:
            row += 1
            label = ttk.Label(content_frame, text=label_text, width=15, anchor="w")
            label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(content_frame, width=width)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")
            setattr(self, attr_name, entry)

        # Phone Number
        row += 1
        phone_number_label = ttk.Label(content_frame, text="Phone Number:", width=15, anchor="w")
        phone_number_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        self.phone_number_entry = ttk.Entry(content_frame, width=20)
        self.phone_number_entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")
        
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
        fields_mapping = {
            'name': self.name_entry,
            'address_line1': self.address_line1_entry,
            'address_line2': self.address_line2_entry,
            'address_line3': self.address_line3_entry,
            'city': self.city_entry,
            'state': self.state_entry,
            'zip_code': self.zip_code_entry,
            'country': self.country_entry,
            'phone_number': self.phone_number_entry
        }
        
        for field, entry in fields_mapping.items():
            value = getattr(self.rec, field, "")
            entry.delete(0, tk.END)
            entry.insert(0, value)
        
        # Set focus to the name field for immediate editing
        self.name_entry.focus_set()
    
    def validate(self):
        """Validate all client fields using validators."""
        # Get trimmed values
        name = self.name_entry.get().strip()
        address_line1 = self.address_line1_entry.get().strip()
        address_line2 = self.address_line2_entry.get().strip()
        address_line3 = self.address_line3_entry.get().strip()
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()
        zip_code = self.zip_code_entry.get().strip()
        country = self.country_entry.get().strip()
        phone_number = self.phone_number_entry.get().strip()
        
        # Validate required fields
        field_validations = {
            'name': (validate_string, [name, "Name", 2, 100]),
            'address_line1': (validate_string, [address_line1, "Address Line 1", 1, 100]),
            'city': (validate_string, [city, "City", 2, 85]),
            'state': (validate_string, [state, "State", 2, 85]),
            'zip_code': (validate_string, [zip_code, "Zip Code", 2, 10]),
            'country': (validate_string, [country, "Country", 2, 75]),
            'phone_number': (validate_phone_number, [phone_number])
        }
        
        # Address lines 2 and 3 are optional, only validate if not empty
        if address_line2:
            field_validations['address_line2'] = (validate_string, [address_line2, "Address Line 2", 0, 100])
        
        if address_line3:
            field_validations['address_line3'] = (validate_string, [address_line3, "Address Line 3", 0, 100])

        errors = {}
        for field, (validator, args) in field_validations.items():
            error = validator(*args) if callable(validator) else None
            if error:
                errors[field] = error
                getattr(self, f"{field}_entry").focus_set()
                break  # Stop at first error

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors.values()))
            return False

        return True
    
    def update_rec(self):
        """Update the record with values from the interface."""
        self.rec.name = self.name_entry.get().strip()
        self.rec.address_line1 = self.address_line1_entry.get().strip()
        self.rec.address_line2 = self.address_line2_entry.get().strip()
        self.rec.address_line3 = self.address_line3_entry.get().strip()
        self.rec.city = self.city_entry.get().strip()
        self.rec.state = self.state_entry.get().strip()
        self.rec.zip_code = self.zip_code_entry.get().strip()
        self.rec.country = self.country_entry.get().strip()
        self.rec.phone_number = self.phone_number_entry.get().strip()
    
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
