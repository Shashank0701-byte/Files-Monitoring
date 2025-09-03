import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file_organizer_config import FILE_EXTENSIONS, DEFAULT_FOLDER

def get_destination_folder(file_extension):
    """Get the destination folder for a file based on its extension."""
    folder_name = FILE_EXTENSIONS.get(file_extension.lower())
    if folder_name:
        if '/' in folder_name:
            return Path.home() / folder_name
        else:
            return Path.home() / folder_name
    else:
        return Path.home() / DEFAULT_FOLDER

def move_file(source_path, file_name):
    """Move file to appropriate folder based on extension."""
    file_path = Path(source_path)
    file_extension = file_path.suffix
    
    if not file_extension:
        print(f"  → Skipping {file_name} (no extension)")
        return None
    
    dest_folder = get_destination_folder(file_extension)
    dest_folder.mkdir(parents=True, exist_ok=True)
    
    dest_path = dest_folder / file_name
    
    # Handle file name conflicts
    counter = 1
    original_dest_path = dest_path
    while dest_path.exists():
        name_part = original_dest_path.stem
        ext_part = original_dest_path.suffix
        dest_path = dest_folder / f"{name_part}_{counter}{ext_part}"
        counter += 1
    
    try:
        shutil.move(str(file_path), str(dest_path))
        return dest_path
    except Exception as e:
        print(f"  → Error moving file {file_name}: {e}")
        return None

class NewFileHandler(FileSystemEventHandler):
    """Handler for file system events that monitors for new files."""
    
    def on_created(self, event):
        """Called when a file or directory is created."""
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            print(f"📄 New file detected: {file_name}")
            
            # Move file to appropriate folder
            downloads_path = Path(event.src_path).parent
            moved_path = move_file(event.src_path, file_name)
            if moved_path:
                relative_path = moved_path.relative_to(Path.home())
                print(f"  ✅ Moved to: ~/{relative_path}")
            else:
                print(f"  ❌ Failed to move file")

def monitor_downloads_folder():
    """Monitor the Downloads folder for new files."""
    # Get the Downloads folder path
    downloads_path = Path.home() / "Downloads"
    
    # Check if Downloads folder exists
    if not downloads_path.exists():
        print(f"Downloads folder not found at: {downloads_path}")
        print("Please make sure the Downloads folder exists.")
        return
    
    print(f"🔍 Monitoring Downloads folder: {downloads_path}")
    print("📦 Files will be automatically organized by type.")
    print("🚀 Press Ctrl+C to stop monitoring...")
    
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