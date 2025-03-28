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
        self.geometry("550x525")
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

        # Fetch reference data
        self.client_names.append("-- Please Select --")
        for c in self.rec_man.clients:
            self.client_names.append(c.name)

        self.airline_names.append("-- Please Select --")
        for c in self.rec_man.airlines:
            self.airline_names.append(c.company_name)

        # Detect and configure system fonts
        import platform
        import tkinter.font as tkfont

        system = platform.system()
        self.default_font = tkfont.nametofont("TkDefaultFont")

        if system == "Windows":
            system_font = "Segoe UI"
        elif system == "Darwin":  # macOS
            system_font = "Helvetica Neue"
        else:  # Linux/Unix
            system_font = "DejaVu Sans"

        self.default_font.configure(family=system_font, size=10)

        # Configure bold font
        self.bold_font = tkfont.Font(font=self.default_font)
        self.bold_font.configure(weight="bold", size=12)
        
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
        """Set up screen layout."""
        # Main content frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame, padding=(15, 10))
        header_frame.pack(fill=tk.X)

        header_label = ttk.Label(
            header_frame,
            text=f"{self.action} Flight",
            font=self.bold_font
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

        self.txt_client_id = ttk.Entry(content_frame, font=self.default_font, width=30)
        #self.txt_client_id.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        self.client_select = ttk.Combobox(content_frame, font=self.default_font, values=self.client_names, width=30)
        self.client_select.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Airline_ID
        lbl_airline_id = ttk.Label(content_frame, text="Airline ID:", width=15, anchor="w")
        lbl_airline_id.grid(row=1,column=0, padx=(50,0), sticky="w")

        self.txt_airline_id = ttk.Entry(content_frame, font=self.default_font, width=30)
        #self.txt_airline_id.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        self.airline_select = ttk.Combobox(content_frame, font=self.default_font, values=self.airline_names, width=30)
        self.airline_select.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Date
        lbl_date = ttk.Label(content_frame, text="Date:", width=15, anchor="nw")
        lbl_date.grid(row=2,column=0, padx=(50,0), sticky="nw")

        dt = datetime.now()
        self.txt_date = Calendar(content_frame, font=self.default_font, selectmode="day", year=dt.year, month=dt.month, day=dt.day)
        self.txt_date.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # Time
        lbl_date = ttk.Label(content_frame, text="Time:", width=15, anchor="nw")
        lbl_date.grid(row=3,column=0, padx=(50,0), sticky="nw")

        self.txt_time = SpinTimePickerModern(content_frame)
        self.txt_time.addAll(constants.HOURS24)  # adds hours clock, minutes and period

        self.txt_time.configureAll(bg="#f0f0f0",
                                   height=1,
                                   fg="#333333",
                                   font=self.default_font,
                                   hoverbg="#e0e0e0",
                                   hovercolor="#1a1a1a",
                                   clickedbg="#d0d0d0",
                                   clickedcolor="#000000")
        self.txt_time.configure_separator(bg="#f0f0f0", fg="#666666")
        self.txt_time.grid(row=3, column=1, padx=5, pady=5, sticky="we")

        current_time = datetime.now()
        self.txt_time.set24Hrs(f"{current_time.hour:02d}")
        self.txt_time.setMins(f"{current_time.minute:02d}")

        # Start City
        lbl_start_city = ttk.Label(content_frame, text="Start City:", width=15, anchor="w")
        lbl_start_city.grid(row=4,column=0, padx=(50,0), sticky="w")

        self.txt_start_city = ttk.Entry(content_frame, font=self.default_font, width=30)
        self.txt_start_city.grid(row=4, column=1, padx=5, pady=5, sticky="we")

        # End City
        lbl_end_city = ttk.Label(content_frame, text="End City:", width=15, anchor="w")
        lbl_end_city.grid(row=5,column=0, padx=(50,0), sticky="w")

        self.txt_end_city = ttk.Entry(content_frame, font=self.default_font, width=30)
        self.txt_end_city.grid(row=5, column=1, padx=5, pady=5, sticky="we")

        # Toolbar with OK and Cancel buttons
        toolbar = ttk.Frame(main_frame, padding=(10, 10))
        toolbar.pack(fill=tk.X)

        cancel_button = ttk.Button(toolbar, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        ok_button = ttk.Button(toolbar, text="OK", width=10, command=self.ok)
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
        try:
            dt = self.txt_date.selection_get()
            new_hr = self.txt_time.hours24()
            new_min = self.txt_time.minutes()
            new_date = datetime(dt.year, dt.month, dt.day, new_hr, new_min)

            client_name = self.client_select.get()
            if (client_name is None or client_name == "" or client_name == "-- Please Select --"):
                messagebox.showerror("Validation failed!", "Please select a valid Client before you continue")
                return False

            airline_name = self.airline_select.get()
            if (airline_name is None or airline_name == "" or airline_name == "-- Please Select --"):
                messagebox.showerror("Validation failed!", "Please select a valid Airline before you continue")
                return False

            if (new_date < datetime.now()):
                messagebox.showerror("Validation failed!", "Flight cannot be booked for past dates")
                return False

            start_city = self.txt_start_city.get().strip()
            if (start_city is None or start_city == ""):
                messagebox.showerror("Validation failed!", "Please select a valid Start City before you continue")
                return False

            end_city = self.txt_end_city.get().strip()
            if (end_city is None or end_city == ""):
                messagebox.showerror("Validation failed!", "Please select a valid End City before you continue")
                return False
        except Exception as e:
            messagebox.showerror("Validation failed!", "The record validation process failed. Please make sure all fields are captured.")
            print(f"Validation failed with exception ({e})")
            return False

        return True


    def update_rec(self):
        """Update the record with values from the interface."""
        if (not self.validate()):
            return

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
