"""
Main entry point for SmartFileOrganizer daemon.

Phase 1: Watchdog Observer Implementation
This module sets up the file system monitoring using watchdog.
"""

import logging
import os
import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

# Import config - works both as module and direct execution
try:
    from .config import Config
except ImportError:
    from config import Config


class SmartFileHandler(FileSystemEventHandler):
    """
    File system event handler for SmartFileOrganizer.
    
    This handler listens to file creation events and will process files
    through the hybrid routing system (to be implemented in later phases).
    """
    
    def __init__(self):
        """Initialize the file handler."""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.pending_files = {}  # Track files that need processing
        
    def on_created(self, event: FileSystemEvent) -> None:
        """
        Handle file creation events.
        
        Args:
            event: FileSystemEvent object containing event information
        """
        if event.is_directory:
            self.logger.debug(f"Directory created: {event.src_path}")
            return
        
        file_path = Path(event.src_path)
        
        # Ignore hidden files and system files
        if file_path.name.startswith('.'):
            self.logger.debug(f"Ignoring hidden file: {file_path.name}")
            return
        
        self.logger.info(f"New file detected: {file_path.name}")
        
        # Schedule file for processing after a delay
        # This ensures the file is fully written before we try to process it
        self.pending_files[str(file_path)] = time.time()
        
        # In Phase 1, we just log the event
        # In later phases, we'll call the hybrid router here
        self.logger.info(f"File queued for processing: {file_path.name}")
        self._log_file_info(file_path)
    
    def on_moved(self, event: FileSystemEvent) -> None:
        """
        Handle file move/rename events.
        
        Args:
            event: FileSystemEvent object containing event information
        """
        if event.is_directory:
            return
        
        self.logger.info(f"File moved/renamed: {event.src_path} -> {event.dest_path}")
    
    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Handle file modification events.
        
        Args:
            event: FileSystemEvent object containing event information
        """
        if event.is_directory:
            return
        
        # Only log significant modifications (not every write operation)
        file_path = Path(event.src_path)
        if str(file_path) in self.pending_files:
            # File is still being written, update timestamp
            self.pending_files[str(file_path)] = time.time()
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        """
        Handle file deletion events.
        
        Args:
            event: FileSystemEvent object containing event information
        """
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if str(file_path) in self.pending_files:
            del self.pending_files[str(file_path)]
            self.logger.info(f"File deleted before processing: {file_path.name}")
    
    def _log_file_info(self, file_path: Path) -> None:
        """
        Log information about a detected file.
        
        Args:
            file_path: Path to the file
        """
        try:
            if file_path.exists():
                stat = file_path.stat()
                self.logger.debug(
                    f"File info - Name: {file_path.name}, "
                    f"Size: {stat.st_size} bytes, "
                    f"Extension: {file_path.suffix}"
                )
        except Exception as e:
            self.logger.warning(f"Could not get file info for {file_path}: {e}")


def setup_logging() -> None:
    """Configure logging for the application."""
    # Ensure log directory exists
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point for the SmartFileOrganizer daemon."""
    # Phase 1.5: Load configuration and setup wizard if needed
    # This MUST happen before logging setup, as it may update LOG_DIR and LOG_FILE
    print("SmartFileOrganizer - Initializing...")
    root_archive_path = Config.load_config()
    
    # Now setup logging with the correct paths
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("SmartFileOrganizer - Phase 1.5: Configuration & Watchdog Observer")
    logger.info("=" * 60)
    
    # Ensure required directories exist
    os.makedirs(root_archive_path, exist_ok=True)
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    # Get watch directory
    watch_dir = Config.get_watch_dir()
    
    if not watch_dir.exists():
        logger.error(f"Watch directory does not exist: {watch_dir}")
        logger.error("Please create the directory or update Config.DEFAULT_WATCH_DIR")
        sys.exit(1)
    
    logger.info(f"Watching directory: {watch_dir}")
    logger.info(f"Root archive path: {root_archive_path}")
    logger.info(f"Log file: {Config.LOG_FILE}")
    logger.info("")
    logger.info("File monitoring started. Press Ctrl+C to stop.")
    logger.info("")
    logger.info(f"NOTE: Root archive path stored for Router: {root_archive_path}")
    logger.info("")
    
    # Create event handler
    # TODO: Pass root_archive_path to handler in Phase 2 for routing
    event_handler = SmartFileHandler()
    
    # Create observer
    observer = Observer()
    observer.schedule(
        event_handler,
        str(watch_dir),
        recursive=Config.WATCH_RECURSIVE
    )
    
    # Start observing
    observer.start()
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("")
        logger.info("Shutting down...")
        observer.stop()
    
    observer.join()
    logger.info("SmartFileOrganizer stopped.")


if __name__ == "__main__":
    main()

