import tkinter as tk

from views.airline_view import AirlineView
from views.client_view import ClientView
from views.flight_view import FlightView


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FlyRecordKeeper - Record Management System")
        self.geometry("900x650")
        self.minsize(800, 600)  # Set minimum window size for usability

        # Frames for layout
        self.menu_frame = tk.Frame(self, width=200, bg="#f0f0f0")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame()
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialize the main content
        self.content = None

        # Setup Menu
        self.create_menu()

        # Load the initial content
        self.load_content("Manage Clients")

        self.mainloop()

    def create_menu(self):
        """Create buttons in the left menu."""
        btn_clients = tk.Button(self.menu_frame, text="Manage Clients", width=20, command=lambda: self.load_content("Manage Clients"))
        btn_clients.pack(pady=2, fill=tk.X)

        btn_airlines = tk.Button(self.menu_frame, text="Manage Airlines", width=20, command=lambda: self.load_content("Manage Airlines"))
        btn_airlines.pack(pady=2)

        btn_flights = tk.Button(self.menu_frame, text="Manage Flights", width=20, command=lambda: self.load_content("Manage Flights"))
        btn_flights.pack(pady=2)

    def load_content(self, content_type):
        """Load content into the right frame."""
        # Only update if the content type is different
        if self.content == content_type:
            return

        self.content = content_type

        # Clear any existing widgets in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        if content_type == "Manage Clients":
            view = ClientView(self.right_frame)
        elif content_type == "Manage Airlines":
            view = AirlineView(self.right_frame)
        elif content_type == "Manage Flights":
            view = FlightView(self.right_frame)
        else:
            return

        
        # Create new content
#        self.create_toolbar()
#        self.create_treeview()

    # def create_toolbar(self):
    #     """Create the toolbar with Add and Search buttons."""
    #     toolbar = tk.Frame(self.right_frame)
    #     toolbar.pack(fill=tk.X)

    #     label = tk.Label(toolbar, text=self.content)
    #     label.pack(pady=(5,10))

    #     add_button = tk.Button(toolbar, text="Add", width=10, command=self.add_item)
    #     add_button.pack(side=tk.LEFT, padx=5)

    #     search_button = tk.Button(toolbar, text="Search", width=10, command=self.search_item)
    #     search_button.pack(side=tk.LEFT, padx=5)

    # def create_treeview(self):
    #     """Create the treeview widget to display data."""
    #     treeview_frame = tk.Frame(self.right_frame)
    #     treeview_frame.pack(fill=tk.BOTH, expand=True)

    #     # Create the treeview widget
    #     treeview = ttk.Treeview(treeview_frame, columns=("ID", "Name", "Age"), show="headings")
        
    #     # Define columns
    #     treeview.heading("ID", text="ID")
    #     treeview.heading("Name", text="Name")
    #     treeview.heading("Age", text="Age")

    #     # Insert some dummy data
    #     data = [
    #         (1, "Alice", 30),
    #         (2, "Bob", 25),
    #         (3, "Charlie", 35),
    #     ]
    #     for item in data:
    #         treeview.insert("", "end", values=item)

    #     treeview.pack(expand=True, fill=tk.BOTH)

    # def add_item(self):
    #     """Handle adding a new item by opening a child window."""
    #     self.open_child_window("Add Item")

    # def search_item(self):
    #     """Handle searching for an item by opening a child window."""
    #     self.open_child_window("Search Item")

    # def open_child_window(self, action):
    #     """Open a modal child window with 'OK' and 'Cancel' buttons."""
    #     child_window = airline_capture.AirlineCapture()
#        child_window = tk.Toplevel(self)
#        child_window.title(action)
#        child_window.geometry("300x200")
        
        # Child window content
#        label = tk.Label(child_window, text=f"{action} - Enter details:")
#        label.pack(pady=20)
        
        # Entry for user input
#        entry = tk.Entry(child_window)
#        entry.pack(pady=10)

        # Toolbar with OK and Cancel buttons
#        toolbar = tk.Frame(child_window)
#        toolbar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

#        ok_button = tk.Button(toolbar, text="OK", width=10, command=lambda: self.on_child_action(child_window, action, entry.get()))
#        ok_button.pack(side=tk.LEFT, padx=5)

#        cancel_button = tk.Button(toolbar, text="Cancel", width=10, command=child_window.destroy)
#        cancel_button.pack(side=tk.LEFT, padx=5)

#    def on_child_action(self, child_window, action, entry_value):
#        """Handle action for OK button (can be Add or Search)."""
#        print(f"{action} - User input: {entry_value}")
        
        # Close the child window after the action
#        child_window.destroy()



