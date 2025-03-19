import tkinter as tk
from tkinter import ttk


class FlightCapture(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Flight Capture")
        self.geometry("400x200")
        
        # Frame for content controls
        content_frame = tk.Frame(self)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)

        # Client_ID
        lbl_client_id = tk.Label(content_frame, text="Client ID:")
        lbl_client_id.grid(row=0,column=0, padx=(50,0))
        
        txt_client_id = tk.Entry(content_frame)
        txt_client_id.grid(row=0, column=1)

        # Airline_ID
        lbl_airline_id = tk.Label(content_frame, text="Airline ID:")
        lbl_airline_id.grid(row=1,column=0, padx=(50,0))
        
        txt_airline_id = tk.Entry(content_frame)
        txt_airline_id.grid(row=1, column=1)

        # Date/Time
        lbl_date = tk.Label(content_frame, text="Date and Time:")
        lbl_date.grid(row=2,column=0, padx=(50,0))
        
        txt_date = tk.Entry(content_frame)
        txt_date.grid(row=2, column=1)

        # Start City
        lbl_start_city = tk.Label(content_frame, text="Start City:")
        lbl_start_city.grid(row=3,column=0, padx=(50,0))
        
        txt_start_city = tk.Entry(content_frame)
        txt_start_city.grid(row=3, column=1)

        # End City
        lbl_end_city = tk.Label(content_frame, text="End City:")
        lbl_end_city.grid(row=4,column=0, padx=(50,0))
        
        txt_end_city = tk.Entry(content_frame)
        txt_end_city.grid(row=4, column=1)

        # Toolbar with OK and Cancel buttons
        toolbar = tk.Frame(self)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        cancel_button = tk.Button(toolbar, text="Cancel", width=10, command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        ok_button = tk.Button(toolbar, text="OK", width=10, command=lambda: self.on_child_action("Capture", entry.get()))
        ok_button.pack(side=tk.RIGHT, padx=5)

    def on_child_action(self, action, entry_value):
        """Handle action for OK button (can be Add or Search)."""
        print(f"{action} - User input: {entry_value}")
        
        # Close the child window after the action
        self.destroy()
