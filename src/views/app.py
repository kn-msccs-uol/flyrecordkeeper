import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys

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

        # Set application icon
        try:
            icon_path = self.get_asset_path('images/flyrecordkeeper_logo_icon.png')
            icon_img = Image.open(icon_path)
            
            # Resize to standard icon size if needed
            icon_img = icon_img.resize((64, 64), Image.LANCZOS)
            
            # Convert to PhotoImage
            icon_photo = ImageTk.PhotoImage(icon_img)
            
            # Set as window icon (works across platforms)
            self.iconphoto(True, icon_photo)
            
        except Exception as e:
            print(f"Error setting application icon: {e}")

        # Detect and configure system fonts
        import platform

        system = platform.system()

        if system == "Windows":
            self.system_font = "Segoe UI"
        elif system == "Darwin":  # macOS
            self.system_font = "Helvetica Neue"
        else:  # Linux/Unix
            self.system_font = "DejaVu Sans"
        
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

    def get_asset_path(self, relative_path):
        """Return a path to an asset file that works regardless of how the app is executed."""
        # Get the directory of the currently executing script
        if getattr(sys, 'frozen', False):
            # If the application is run as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # If the application is run from Python interpreter
            # Get path to views directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up to src directory
            src_dir = os.path.dirname(current_dir)
            # Go up to project root
            base_path = os.path.dirname(src_dir)
            
        return os.path.join(base_path, 'assets', relative_path)
    
    def setup_styles(self):
        """Configure application styling using ttk."""
        self.style = ttk.Style(self)
        
        # Use a more modern theme if available
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        
        # Configure styles for different widget types
        self.style.configure('NavLabel.TLabel', font=(self.system_font, 12, 'italic'))
        self.style.configure('NavButton.TButton', padding=8, font=(self.system_font, 11))
        self.style.configure('Header.TLabel', font=('Georgia', 16, 'bold', 'italic'))
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
        try:
            # Load and resize the logo image
            logo_path = self.get_asset_path('images/flyrecordkeeper_logo.png')
            original_logo = Image.open(logo_path)
            
            # Calculate appropriate size while maintaining aspect ratio
            # Assuming sidebar width of ~180px, so logo should be ~160px wide
            width, height = original_logo.size
            new_width = 160
            new_height = int(height * (new_width / width))
            
            # Resize image with high quality
            resized_logo = original_logo.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage for Tkinter
            self.logo_image = ImageTk.PhotoImage(resized_logo)
            
            # Display the logo
            logo_label = ttk.Label(self.menu_frame, image=self.logo_image)
            logo_label.pack(pady=(10, 15), anchor='center')
            
        except Exception as e:
            # Fallback to text if image loading fails
            print(f"Error loading logo: {e}")
            logo_label = ttk.Label(self.menu_frame, text="FlyRecordKeeper", style='Header.TLabel')
            logo_label.pack(pady=(0, 15), anchor='center')
        
        # Add a separator
        separator1 = ttk.Separator(self.menu_frame, orient='horizontal')
        separator1.pack(fill='x', pady=5)
        
        # Navigation section
        nav_label = ttk.Label(self.menu_frame, text="Navigation", style='NavLabel.TLabel')
        nav_label.pack(anchor='w', pady=5)
        
        # Add a separator
        separator2 = ttk.Separator(self.menu_frame, orient='horizontal')
        separator2.pack(fill='x', pady=5)
        
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
        separator3 = ttk.Separator(self.main_frame, orient='vertical')
        separator3.pack(side=tk.LEFT, fill=tk.Y, padx=2)
        
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
                view = ClientView(self.content_frame, self.update_status)
                self.highlight_active_nav("Manage Clients")
                
            elif content_type == "Manage Airlines":
                view = AirlineView(self.content_frame, self.update_status)
                self.highlight_active_nav("Manage Airlines")
                
            elif content_type == "Manage Flights":
                view = FlightView(self.content_frame, self.update_status)
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
        """Update the status bar with a message and timestamp."""
        import datetime

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_bar.config(text=f"[{timestamp}] {message}")
        self.update_idletasks()
    
    def on_closing(self):
        """Handle application closing with confirmation."""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            # IMPLEMENT on-close save operations HERE
            self.update_status("Saving data...")
            self.destroy()
