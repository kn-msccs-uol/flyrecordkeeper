import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date


class FlightCapture(tk.Toplevel):
    def __init__(self, rec, action="Add"):
        super().__init__()

        self.title(f"{action} Flight Record")
        self.geometry("500x300")
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
        # Main content frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame, padding=(15, 10))
        header_frame.pack(fill=tk.X)
        
        header_label = ttk.Label(
            header_frame,
            text=f"{self.action} Flight", 
            font=('Segoe UI', 11, 'bold')
        )
        header_label.pack(anchor=tk.W)
        
        # Separator after header
        sep = ttk.Separator(main_frame, orient='horizontal')
        sep.pack(fill='x')
        
        # Frame for content controls
        content_frame = ttk.Frame(main_frame, padding=(20, 15))
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Client_ID
        lbl_client_id = ttk.Label(content_frame, text="Client ID:", width=15, anchor="w")
        lbl_client_id.grid(row=0,column=0, padx=(50,0), sticky="w")
        
        self.txt_client_id = ttk.Entry(content_frame, width=30)
        self.txt_client_id.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Airline_ID
        lbl_airline_id = ttk.Label(content_frame, text="Airline ID:", width=15, anchor="w")
        lbl_airline_id.grid(row=1,column=0, padx=(50,0), sticky="w")
        
        self.txt_airline_id = ttk.Entry(content_frame, width=30)
        self.txt_airline_id.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Date/Time
        lbl_date = ttk.Label(content_frame, text="Date and Time:", width=15, anchor="w")
        lbl_date.grid(row=2,column=0, padx=(50,0), sticky="w")
        
        self.txt_date = ttk.Entry(content_frame, width=30) #DateEntry(content_frame, selectmode="day", year=dt.year, month=dt.month, day=dt.day) 
        self.txt_date.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # Start City
        lbl_start_city = ttk.Label(content_frame, text="Start City:", width=15, anchor="w")
        lbl_start_city.grid(row=3,column=0, padx=(50,0), sticky="w")
        
        self.txt_start_city = ttk.Entry(content_frame, width=30)
        self.txt_start_city.grid(row=3, column=1, padx=5, pady=5, sticky="we")

        # End City
        lbl_end_city = ttk.Label(content_frame, text="End City:", width=15, anchor="w")
        lbl_end_city.grid(row=4,column=0, padx=(50,0), sticky="w")
        
        self.txt_end_city = ttk.Entry(content_frame, width=30)
        self.txt_end_city.grid(row=4, column=1, padx=5, pady=5, sticky="we")

        # Toolbar with OK and Cancel buttons
        toolbar = ttk.Frame(main_frame, padding=(10, 10))
        toolbar.pack(fill=tk.X)

        cancel_button = tk.Button(toolbar, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        ok_button = tk.Button(toolbar, text="OK", width=10, command=self.ok)
        ok_button.pack(side=tk.RIGHT, padx=5)


    def bind_rec(self):
        """Bind record data to the interface elements."""
        self.txt_client_id.insert(0, self.rec.client_id)
        self.txt_airline_id.insert(0, self.rec.airline_id)
        self.txt_date.insert(0, self.rec.date)
        self.txt_start_city.insert(0, self.rec.start_city)
        self.txt_end_city.insert(0, self.rec.end_city)
        
        # Set focus to the name field for immediate editing
        self.txt_client_id.focus_set()
    
    def validate(self):
        """Validate the input data before accepting it."""
        #company_name = self.name_entry.get().strip()
        
        #if not company_name:
        #    messagebox.showerror("Validation Error", "Company Name cannot be empty.")
        #    self.name_entry.focus_set()
        #    return False
        
        #if len(company_name) > 100:
        #    messagebox.showerror("Validation Error", "Company Name cannot exceed 100 characters.")
        #    self.name_entry.focus_set()
        #    return False
        
        return True
    

    def update_rec(self):
        """Update the record with values from the interface."""
        self.rec.client_id = self.txt_client_id.get().strip()
        self.rec.airline_id = self.txt_airline_id.get().strip()
        self.rec.date = self.txt_date.get().strip()
        self.rec.start_city = self.txt_start_city.get().strip()
        self.rec.end_city = self.txt_end_city.get().strip()
    
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
        self.txt_airline_id.focus_force()
        self.wait_window()
        return (self.result, self.rec)
