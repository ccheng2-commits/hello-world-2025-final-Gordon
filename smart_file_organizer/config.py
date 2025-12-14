"""
Configuration module for SmartFileOrganizer.

This module contains all configuration settings for the file organization daemon.
Handles configuration loading from JSON and setup wizard for first-time users.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class Config:
    """Configuration class for SmartFileOrganizer."""
    
    # Configuration file path
    CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".smart_file_organizer", "config.json")
    CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".smart_file_organizer")
    
    # Default watch directory (macOS Desktop)
    DEFAULT_WATCH_DIR = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Archive base directory (where organized files will be moved)
    # This will be loaded from config.json or set via Setup Wizard
    DEFAULT_ARCHIVE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "SmartFileArchive")
    
    # Root archive path (loaded from config.json)
    ROOT_ARCHIVE_PATH: Optional[str] = None
    
    # Logging configuration
    LOG_DIR = os.path.join(os.path.expanduser("~"), "Documents", "SmartFileArchive", "_logs")
    LOG_FILE = os.path.join(LOG_DIR, "organizer.log")
    
    # Watchdog settings
    WATCH_RECURSIVE = False  # Only watch the top-level directory initially
    
    # File processing settings
    PROCESS_DELAY_SECONDS = 2.0  # Wait time before processing a file (to ensure file is fully written)
    
    # Ollama/Qwen settings (for Phase 4)
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "qwen2.5"
    
    # Prefix rules (Layer 1 - Fast Track)
    # Format: {"prefix": "destination_folder"}
    PREFIX_RULES: Dict[str, str] = {
        # Example: Files starting with "pcom_" go to "Projects/Communication"
        "pcom_": "Projects/Communication",
        # Add more prefix rules here in Phase 2
    }
    
    # Regex rules (Layer 1 - Fast Track)
    # Format: List of tuples: (pattern, destination_folder)
    REGEX_RULES: List[tuple] = [
        # Example: Files matching pattern go to specific folder
        # (r"^invoice_\d{4}-\d{2}-\d{2}", "Finance/Invoices"),
        # Add more regex rules here in Phase 2
    ]
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        # Use ROOT_ARCHIVE_PATH if available, otherwise use default
        archive_dir = cls.ROOT_ARCHIVE_PATH or cls.DEFAULT_ARCHIVE_DIR
        os.makedirs(archive_dir, exist_ok=True)
        os.makedirs(cls.LOG_DIR, exist_ok=True)
    
    @classmethod
    def get_watch_dir(cls) -> Path:
        """Get the watch directory as a Path object."""
        return Path(cls.DEFAULT_WATCH_DIR)
    
    @classmethod
    def get_archive_dir(cls) -> Path:
        """Get the archive directory as a Path object."""
        if cls.ROOT_ARCHIVE_PATH:
            return Path(cls.ROOT_ARCHIVE_PATH)
        return Path(cls.DEFAULT_ARCHIVE_DIR)
    
    @classmethod
    def ensure_config_dir(cls) -> None:
        """Ensure the configuration directory exists."""
        os.makedirs(cls.CONFIG_DIR, exist_ok=True)
    
    @classmethod
    def setup_wizard(cls) -> str:
        """
        Show a GUI dialog to let the user select the root archive path.
        
        Returns:
            str: The selected directory path
            
        Raises:
            SystemExit: If user cancels or tkinter is not available
        """
        if not TKINTER_AVAILABLE:
            print("ERROR: tkinter is not available. Cannot show setup wizard.")
            print("Please install tkinter or create config.json manually at:")
            print(f"  {cls.CONFIG_FILE}")
            sys.exit(1)
        
        # Create a root window (hidden)
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        root.attributes('-topmost', True)  # Bring to front
        
        # Show directory selection dialog
        print("\n" + "=" * 60)
        print("SmartFileOrganizer - First Time Setup")
        print("=" * 60)
        print("\nPlease select the folder where you want AI to organize your files.")
        print("(A file picker window should appear...)\n")
        
        selected_path = filedialog.askdirectory(
            title="Select the folder where you want AI to organize your files",
            initialdir=os.path.expanduser("~")
        )
        
        root.destroy()
        
        if not selected_path:
            print("\nERROR: Setup cancelled. No directory selected.")
            print("SmartFileOrganizer cannot run without a target directory.")
            sys.exit(1)
        
        # Validate the selected path
        if not os.path.isdir(selected_path):
            print(f"\nERROR: Invalid directory: {selected_path}")
            sys.exit(1)
        
        print(f"✓ Selected directory: {selected_path}\n")
        return selected_path
    
    @classmethod
    def load_config(cls) -> str:
        """
        Load configuration from config.json or trigger setup wizard.
        
        Returns:
            str: The root archive path
            
        Raises:
            SystemExit: If setup is cancelled or path is invalid
        """
        cls.ensure_config_dir()
        
        # Check if config.json exists
        config_path = Path(cls.CONFIG_FILE)
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                root_path = config_data.get('root_archive_path')
                
                if not root_path:
                    print("WARNING: config.json exists but 'root_archive_path' is missing.")
                    print("Triggering setup wizard...\n")
                    root_path = cls.setup_wizard()
                else:
                    # Validate the path
                    if not os.path.isdir(root_path):
                        print(f"WARNING: Configured path does not exist: {root_path}")
                        print("Triggering setup wizard...\n")
                        root_path = cls.setup_wizard()
                    else:
                        print(f"✓ Loaded configuration from: {config_path}")
                        print(f"✓ Root archive path: {root_path}\n")
                
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid JSON in config.json: {e}")
                print("Triggering setup wizard...\n")
                root_path = cls.setup_wizard()
            except Exception as e:
                print(f"ERROR: Failed to load config.json: {e}")
                print("Triggering setup wizard...\n")
                root_path = cls.setup_wizard()
        else:
            # Config file doesn't exist, trigger setup wizard
            print("First time setup detected. No config.json found.")
            print("Triggering setup wizard...\n")
            root_path = cls.setup_wizard()
        
        # Save the configuration
        cls.save_config(root_path)
        
        # Store in class variable
        cls.ROOT_ARCHIVE_PATH = root_path
        
        # Update log directory to be relative to root archive path
        cls.LOG_DIR = os.path.join(root_path, "_logs")
        cls.LOG_FILE = os.path.join(cls.LOG_DIR, "organizer.log")
        
        return root_path
    
    @classmethod
    def save_config(cls, root_archive_path: str) -> None:
        """
        Save configuration to config.json.
        
        Args:
            root_archive_path: The root archive path to save
        """
        cls.ensure_config_dir()
        
        config_data = {
            'root_archive_path': root_archive_path,
            'version': '1.0'
        }
        
        config_path = Path(cls.CONFIG_FILE)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Configuration saved to: {config_path}\n")
        except Exception as e:
            print(f"ERROR: Failed to save configuration: {e}")
            sys.exit(1)

