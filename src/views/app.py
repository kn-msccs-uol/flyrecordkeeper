import tkinter as tk
from tkinter import ttk, messagebox

from views.airline_view import AirlineView
from views.client_view import ClientView
from views.flight_view import FlightView

class App(tk.Tk):
    """
    Main application window for FlyRecordKeeper.
    Handles the overall application layout and navigation between different record views.
    """
    def __init__(self):
        super().__init__()
        self.title("FlyRecordKeeper - Record Management System")
        self.geometry("900x650")
        self.minsize(800, 600)  # Set minimum window size for usability
        
        # Apply styling for a more modern appearance
        self.setup_styles()
        
        # Set up the main application layout
        self.setup_layout()
        
        # Initialize tracking variables
        self.current_view = None
        
        # Load the initial content
        self.load_content("Manage Clients")
        
        # Set up keyboard shortcuts
        self.bind_shortcuts()
        
        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.mainloop()
    
    def setup_styles(self):
        """Configure application styling using ttk."""
        self.style = ttk.Style(self)
        
        # Use a more modern theme if available
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        
        # Configure styles for different widget types
        self.style.configure('NavButton.TButton', padding=8, font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        self.style.configure('StatusBar.TLabel', padding=2, relief=tk.SUNKEN)
    
    def setup_layout(self):
        """Create the main application layout structure."""
        # Main container frame
        self.main_frame = ttk.Frame(self, padding=5)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left navigation panel
        self.menu_frame = ttk.Frame(self.main_frame, width=200, padding=5)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # App title/logo
        logo_label = ttk.Label(self.menu_frame, text="FlyRecordKeeper", style='Header.TLabel')
        logo_label.pack(pady=(0, 15), anchor='center')
        
        # Navigation section
        nav_label = ttk.Label(self.menu_frame, text="Navigation")
        nav_label.pack(anchor='w', pady=(0, 5))
        
        # Add a separator
        separator = ttk.Separator(self.menu_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
        
        # Create navigation buttons
        self.create_menu()
        
        # Spacer to push exit button to bottom
        spacer = ttk.Frame(self.menu_frame)
        spacer.pack(fill=tk.Y, expand=True)
        
        # Exit button
        exit_button = ttk.Button(
            self.menu_frame, 
            text="Exit", 
            command=self.on_closing,
            style='NavButton.TButton',
            width=20
        )
        exit_button.pack(pady=10, fill=tk.X)
        
        # Add vertical separator
        separator = ttk.Separator(self.main_frame, orient='vertical')
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=2)
        
        # Content frame for views
        self.content_frame = ttk.Frame(self.main_frame, padding=5)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = ttk.Label(
            self, 
            text="Ready", 
            style='StatusBar.TLabel',
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        """Create navigation buttons in the left menu."""
        # Dictionary to track navigation buttons
        self.nav_buttons = {}
        
        # Clients management button
        btn_clients = ttk.Button(
            self.menu_frame, 
            text="Manage Clients", 
            command=lambda: self.load_content("Manage Clients"),
            style='NavButton.TButton',
            width=20
        )
        btn_clients.pack(pady=2, fill=tk.X)
        self.nav_buttons["Manage Clients"] = btn_clients
        
        # Airlines management button
        btn_airlines = ttk.Button(
            self.menu_frame, 
            text="Manage Airlines", 
            command=lambda: self.load_content("Manage Airlines"),
            style='NavButton.TButton',
            width=20
        )
        btn_airlines.pack(pady=2, fill=tk.X)
        self.nav_buttons["Manage Airlines"] = btn_airlines
        
        # Flights management button
        btn_flights = ttk.Button(
            self.menu_frame, 
            text="Manage Flights", 
            command=lambda: self.load_content("Manage Flights"),
            style='NavButton.TButton',
            width=20
        )
        btn_flights.pack(pady=2, fill=tk.X)
        self.nav_buttons["Manage Flights"] = btn_flights
    
    def load_content(self, content_type):
        """
        Load the appropriate view into the content frame.
        
        Args:
            content_type: String indicating which view to load
        """
        # Only update if content type is different
        if self.current_view == content_type:
            return
        
        self.current_view = content_type
        self.update_status(f"Loading {content_type}...")
        
        try:
            # Clear any existing widgets in the right frame
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Load the appropriate view
            if content_type == "Manage Clients":
                view = ClientView(self.content_frame)
                self.highlight_active_nav("Manage Clients")
                
            elif content_type == "Manage Airlines":
                view = FlightView(self.content_frame)
                self.highlight_active_nav("Manage Airlines")
                
            elif content_type == "Manage Flights":
                view = AirlineView(self.content_frame)
                self.highlight_active_nav("Manage Flights")
                
            else:
                self.update_status("Unknown content type")
                return
            
            self.update_status(f"{content_type} loaded successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load {content_type}: {str(e)}")
            self.update_status(f"Error: Failed to load {content_type}")
    
    def highlight_active_nav(self, active_item):
        """Highlight the active navigation button."""
        for item, button in self.nav_buttons.items():
            if item == active_item:
                button.state(['pressed'])  # Visual indicator for active view
            else:
                button.state(['!pressed'])
    
    def bind_shortcuts(self):
        """Set up keyboard shortcuts for navigation."""
        self.bind("<Alt-c>", lambda e: self.load_content("Manage Clients"))
        self.bind("<Alt-a>", lambda e: self.load_content("Manage Airlines"))
        self.bind("<Alt-f>", lambda e: self.load_content("Manage Flights"))
        self.bind("<Escape>", lambda e: self.on_closing())
    
    def update_status(self, message):
        """Update the status bar with a message."""
        self.status_bar.config(text=message)
        self.update_idletasks()
    
    def on_closing(self):
        """Handle application closing with confirmation."""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            # IMPLEMENT on-close save operations HERE
            self.update_status("Saving data...")
            self.destroy()
