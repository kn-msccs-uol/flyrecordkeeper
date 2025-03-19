import tkinter as tk
from tkinter import ttk


class ClientCapture(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Client Capture")
        self.geometry("400x400")
        
        # Frame for content controls
        content_frame = tk.Frame(self)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)

        # ID
        lbl_id = tk.Label(content_frame, text="ID:")
        lbl_id.grid(row=0,column=0, padx=(50,0))
        
        txt_id = tk.Entry(content_frame)
        txt_id.grid(row=0, column=1)

        # Type
        lbl_type = tk.Label(content_frame, text="Type:")
        lbl_type.grid(row=1,column=0, padx=(50,0))
        
        txt_type = tk.Entry(content_frame)
        txt_type.grid(row=1, column=1)

        # Name
        lbl_name = tk.Label(content_frame, text="Name:")
        lbl_name.grid(row=2,column=0, padx=(50,0))
        
        txt_name = tk.Entry(content_frame)
        txt_name.grid(row=2, column=1)

        # Address Line 1
        lbl_add_1 = tk.Label(content_frame, text="Address Line 1:")
        lbl_add_1.grid(row=3,column=0, padx=(50,0))
        
        txt_add_1 = tk.Entry(content_frame)
        txt_add_1.grid(row=3, column=1)

        # Address Line 2
        lbl_add_2 = tk.Label(content_frame, text="Address Line 2:")
        lbl_add_2.grid(row=4,column=0, padx=(50,0))
        
        txt_add_2 = tk.Entry(content_frame)
        txt_add_2.grid(row=4, column=1)

        # Address Line 3
        lbl_add_3 = tk.Label(content_frame, text="Address Line 3:")
        lbl_add_3.grid(row=5,column=0, padx=(50,0))
        
        txt_add_3 = tk.Entry(content_frame)
        txt_add_3.grid(row=5, column=1)

        # City
        lbl_city = tk.Label(content_frame, text="City:")
        lbl_city.grid(row=6,column=0, padx=(50,0))
        
        txt_city = tk.Entry(content_frame)
        txt_city.grid(row=6, column=1)

        # State
        lbl_state = tk.Label(content_frame, text="State:")
        lbl_state.grid(row=7,column=0, padx=(50,0))
        
        txt_state = tk.Entry(content_frame)
        txt_state.grid(row=7, column=1)

        # Zip Code
        lbl_zipcode = tk.Label(content_frame, text="Zip Code:")
        lbl_zipcode.grid(row=8,column=0, padx=(50,0))
        
        txt_zipcode = tk.Entry(content_frame)
        txt_zipcode.grid(row=8, column=1)

        # Country
        lbl_country = tk.Label(content_frame, text="Country:")
        lbl_country.grid(row=9,column=0, padx=(50,0))
        
        txt_country = tk.Entry(content_frame)
        txt_country.grid(row=9, column=1)

        # Phone Number
        lbl_phn = tk.Label(content_frame, text="Phone Number:")
        lbl_phn.grid(row=10,column=0, padx=(50,0))
        
        txt_phn = tk.Entry(content_frame)
        txt_phn.grid(row=10, column=1)

        # Toolbar with OK and Cancel buttons
        toolbar = tk.Frame(self)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        cancel_button = tk.Button(toolbar, text="Cancel", width=10, command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        ok_button = tk.Button(toolbar, text="OK", width=10, command=lambda: self.on_child_action("Capture", txt_id.get()))
        ok_button.pack(side=tk.RIGHT, padx=5)

    def on_child_action(self, action, entry_value):
        """Handle action for OK button (can be Add or Search)."""
        print(f"{action} - User input: {entry_value}")
        
        # Close the child window after the action
        self.destroy()
