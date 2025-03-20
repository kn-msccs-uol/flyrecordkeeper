import tkinter as tk
from tkinter import ttk


class AirlineCapture(tk.Toplevel):
    def __init__(self, rec):
        super().__init__()

        self.title("Airline Capture")
        self.geometry("400x150")
        self.rec = rec
        self.result = False
        
        # Frame for content controls
        content_frame = tk.Frame(self)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)

        # ID
        lbl_id = tk.Label(content_frame, text="ID:", anchor="w")
        lbl_id.grid(row=0,column=0, padx=(50,0), sticky="nsew")
        
        self.txt_id_val = tk.Label(content_frame, anchor="w", text=self.rec.id)
        self.txt_id_val.grid(row=0, column=1, sticky="nsew")

        # Company Name
        lbl_name = tk.Label(content_frame, text="Company Name:", anchor="w")
        lbl_name.grid(row=2,column=0, padx=(50,0), sticky="nsew")
        
        self.txt_name = tk.Entry(content_frame,textvariable=self.rec.company_name)
        self.txt_name.grid(row=2, column=1)

        # Toolbar with OK and Cancel buttons
        toolbar = tk.Frame(self)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        cancel_button = tk.Button(toolbar, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        ok_button = tk.Button(toolbar, text="OK", width=10, command=self.ok)
        ok_button.pack(side=tk.RIGHT, padx=5)

        self.bind_rec()

    def bind_rec(self):
        """Bind data on load"""
        self.txt_name.insert(0, self.rec.company_name)

    def update_rec(self):
        """Update the record with inputs from the user"""
        self.rec.company_name = self.txt_name.get()


    def cancel(self):
        """Handle action for OK button (can be Add or Search)."""
        self.result = False

        self.destroy()


    def ok(self):
        """Handle action for OK button (can be Add or Search)."""
        self.update_rec()

        self.result = True

        # Close the child window after the action
        self.destroy()


    def show(self):
        """Handle Show method and return record result"""
        self.wm_deiconify()
        self.txt_name.focus_force()
        self.wait_window()
        return (self.result, self.rec)