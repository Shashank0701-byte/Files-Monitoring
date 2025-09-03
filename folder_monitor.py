import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NewFileHandler(FileSystemEventHandler):
    """Handler for file system events that monitors for new files."""
    
    def on_created(self, event):
        """Called when a file or directory is created."""
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            print(f"New file detected: {file_name}")

def monitor_downloads_folder():
    """Monitor the Downloads folder for new files."""
    # Get the Downloads folder path
    downloads_path = Path.home() / "Downloads"
    
    # Check if Downloads folder exists
    if not downloads_path.exists():
        print(f"Downloads folder not found at: {downloads_path}")
        print("Please make sure the Downloads folder exists.")
        return
    
    print(f"Monitoring Downloads folder: {downloads_path}")
    print("Press Ctrl+C to stop monitoring...")
    
    # Create event handler and observer
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, str(downloads_path), recursive=False)
    
    # Start monitoring
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file monitor...")
        observer.stop()
    
    observer.join()
    print("File monitoring stopped.")

if __name__ == "__main__":
    monitor_downloads_folder()