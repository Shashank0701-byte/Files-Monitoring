import os
import time
from pathlib import Path

def monitor_downloads_folder():
    """Monitor the Downloads folder for new files using polling."""
    # Get the Downloads folder path
    downloads_path = Path.home() / "Downloads"
    
    # Check if Downloads folder exists
    if not downloads_path.exists():
        print(f"Downloads folder not found at: {downloads_path}")
        print("Please make sure the Downloads folder exists.")
        return
    
    print(f"Monitoring Downloads folder: {downloads_path}")
    print("Press Ctrl+C to stop monitoring...")
    
    # Get initial set of files
    previous_files = set()
    try:
        previous_files = set(os.listdir(downloads_path))
    except OSError as e:
        print(f"Error accessing Downloads folder: {e}")
        return
    
    try:
        while True:
            time.sleep(1)  # Check every second
            
            try:
                # Get current files
                current_files = set(os.listdir(downloads_path))
                
                # Find new files
                new_files = current_files - previous_files
                
                # Print new files
                for file_name in new_files:
                    file_path = downloads_path / file_name
                    if file_path.is_file():  # Only report actual files, not directories
                        print(f"New file detected: {file_name}")
                
                # Update previous files set
                previous_files = current_files
                
            except OSError as e:
                print(f"Error checking folder: {e}")
                time.sleep(5)  # Wait longer if there's an error
                
    except KeyboardInterrupt:
        print("\nStopping file monitor...")
    
    print("File monitoring stopped.")

if __name__ == "__main__":
    monitor_downloads_folder()