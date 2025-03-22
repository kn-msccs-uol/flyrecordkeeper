import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
from models import record_manager
from models import flight_record

class FlightCapture(tk.Toplevel):
    def __init__(self, rec_man: record_manager.RecordManager, rec: flight_record.FlightRecord, action="Add"):
        super().__init__()

        self.title(f"{action} Flight Record")
        self.geometry("550x450")
        self.resizable(False, False)
        
        # Make it modal
        self.transient()
        self.grab_set()

        # Store the record and initialize result
        self.rec_man = rec_man
        self.rec = rec
        self.result = False
        self.action = action
        self.client_names = []
        self.airline_names = []

        #fetch reference data
        self.client_names.append("-- Please Select --")
        for c in self.rec_man.clients:
            self.client_names.append(c.name)
        
        self.airline_names.append("-- Please Select --")
        for c in self.rec_man.airlines:
            self.airline_names.append(c.company_name)
        
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
            font=(12)
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
        #self.txt_client_id.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        self.client_select = ttk.Combobox(content_frame, values=self.client_names, width=30)
        self.client_select.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Airline_ID
        lbl_airline_id = ttk.Label(content_frame, text="Airline ID:", width=15, anchor="w")
        lbl_airline_id.grid(row=1,column=0, padx=(50,0), sticky="w")
        
        self.txt_airline_id = ttk.Entry(content_frame, width=30)
        #self.txt_airline_id.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        self.airline_select = ttk.Combobox(content_frame, values=self.airline_names, width=30)
        self.airline_select.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Date
        lbl_date = ttk.Label(content_frame, text="Date:", width=15, anchor="nw")
        lbl_date.grid(row=2,column=0, padx=(50,0), sticky="nw")
        
        dt = datetime.now()
        self.txt_date = Calendar(content_frame, selectmode="day", year=dt.year, month=dt.month, day=dt.day)
        self.txt_date.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # Time
        lbl_date = ttk.Label(content_frame, text="Time:", width=15, anchor="nw")
        lbl_date.grid(row=3,column=0, padx=(50,0), sticky="nw")
        
        self.txt_time = SpinTimePickerModern(content_frame)
        self.txt_time.addAll(constants.HOURS24)  # adds hours clock, minutes and period
        self.txt_time.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Segoe UI", 11), hoverbg="#404040",
                                hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
        self.txt_time.configure_separator(bg="#404040", fg="#ffffff")
        self.txt_time.grid(row=3, column=1, padx=5, pady=5, sticky="we")


        # Start City
        lbl_start_city = ttk.Label(content_frame, text="Start City:", width=15, anchor="w")
        lbl_start_city.grid(row=4,column=0, padx=(50,0), sticky="w")
        
        self.txt_start_city = ttk.Entry(content_frame, width=30)
        self.txt_start_city.grid(row=4, column=1, padx=5, pady=5, sticky="we")

        # End City
        lbl_end_city = ttk.Label(content_frame, text="End City:", width=15, anchor="w")
        lbl_end_city.grid(row=5,column=0, padx=(50,0), sticky="w")
        
        self.txt_end_city = ttk.Entry(content_frame, width=30)
        self.txt_end_city.grid(row=5, column=1, padx=5, pady=5, sticky="we")

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
        self.txt_date.selection_set(self.rec.date.date())
        self.txt_time.set24Hrs(self.rec.date.hour)
        self.txt_time.setMins(self.rec.date.minute)
        self.txt_start_city.insert(0, self.rec.start_city)
        self.txt_end_city.insert(0, self.rec.end_city)
        
        client_idx = 0
        if (self.rec.client_name and self.rec.client_name != ""):
            client_idx = self.client_names.index(self.rec.client_name)

        airline_idx = 0
        if (self.rec.airline_name and self.rec.airline_name != ""):
            airline_idx = self.airline_names.index(self.rec.airline_name)

        self.client_select.current(client_idx)
        self.airline_select.current(airline_idx)

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
    
    # def index_of(self, cbo: ttk.ComboBox, search_val: str):
    #     #for v in cbo.values()):


    #     return 0
    

    def update_rec(self):
        """Update the record with values from the interface."""
        dt = self.txt_date.selection_get()
        new_hr = self.txt_time.hours24()
        new_min = self.txt_time.minutes()
        new_date = datetime(dt.year, dt.month, dt.day, new_hr, new_min)

        self.rec.client_id = self.txt_client_id.get().strip()
        self.rec.client_name = self.client_select.get()
        self.rec.airline_id = self.txt_airline_id.get().strip()
        self.rec.airline_name = self.airline_select.get()
        self.rec.date = new_date
        self.rec.start_city = self.txt_start_city.get().strip()
        self.rec.end_city = self.txt_end_city.get().strip()

        self.resolve_ids()


    def resolve_ids(self):
        """Resolve id's for combo box selections."""
        for c in self.rec_man.clients:
            if self.rec.client_name == c.name:
                self.rec.client_id = c.id
                break

        for a in self.rec_man.airlines:
            if self.rec.airline_name == a.company_name:
                self.rec.airline_id = a.id
                break


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
