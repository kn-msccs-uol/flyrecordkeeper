import tkinter as tk
from tkinter import ttk


class AirlineCapture(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Airline Capture")
        self.geometry("400x150")
        
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

        # Company Name
        lbl_name = tk.Label(content_frame, text="Company Name:")
        lbl_name.grid(row=2,column=0, padx=(50,0))
        
        txt_name = tk.Entry(content_frame)
        txt_name.grid(row=2, column=1)

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
