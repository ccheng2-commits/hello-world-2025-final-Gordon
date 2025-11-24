"""
IRIS#1 - Digital Biometrics
Watches the incoming folder for new iris photos and triggers processing pipeline.
For MVP: simple file watcher. Later: integrate with camera automation.
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
from backend.config import INCOMING_DIR, WATCH_PATTERNS
from backend.iris_processor import process_iris_photo
from backend.fft_pipeline import process_iris_fft
from backend.latent_code import generate_latent_code, save_latent_code


class IrisPhotoHandler(FileSystemEventHandler):
    """
    Handles new file events in the incoming folder.
    When a new photo appears, triggers the full processing pipeline.
    """
    
    def __init__(self):
        self.processed_files = set()  # Track already processed files
    
    def on_created(self, event):
        """Called when a new file is created"""
        if not event.is_directory:
            self.process_file(event.src_path)
    
    def on_moved(self, event):
        """Called when a file is moved (e.g., camera saves to folder)"""
        if not event.is_directory:
            self.process_file(event.dest_path)
    
    def process_file(self, file_path):
        """
        Process a new iris photo through the full pipeline.
        """
        file_path = Path(file_path)
        
        # Check if it's an image file we care about
        if not any(file_path.name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            return
        
        # Avoid processing the same file twice
        if str(file_path) in self.processed_files:
            return
        
        # Wait a moment for file to be fully written
        time.sleep(0.5)
        
        if not file_path.exists():
            return
        
        print(f"\n📸 New photo detected: {file_path.name}")
        print("Starting processing pipeline...")
        
        try:
            # Step 1: Process iris (crop)
            processed_path = process_iris_photo(file_path)
            
            # Step 2: Compute FFT
            fft_path, fft_spectrum = process_iris_fft(processed_path)
            
            # Step 3: Generate latent code
            latent_code, features, seed = generate_latent_code(processed_path, fft_spectrum)
            
            # Step 4: Save latent code
            save_latent_code(latent_code, features, seed)
            
            print(f"✅ Processing complete!")
            print(f"   Latent code: {latent_code}")
            
            # Mark as processed
            self.processed_files.add(str(file_path))
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
            import traceback
            traceback.print_exc()


def start_watching():
    """
    Start watching the incoming folder for new photos.
    """
    print(f"👀 Watching folder: {INCOMING_DIR}")
    print("   Waiting for new iris photos...")
    print("   (Place test images in data/incoming/ to test)")
    print("   Press Ctrl+C to stop\n")
    
    event_handler = IrisPhotoHandler()
    observer = Observer()
    observer.schedule(event_handler, str(INCOMING_DIR), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 Stopped watching folder")
    
    observer.join()


if __name__ == "__main__":
    start_watching()

