import os
import time
import shutil
from pathlib import Path
from file_organizer_config import FILE_EXTENSIONS, DEFAULT_FOLDER

def get_destination_folder(file_extension):
    """Get the destination folder for a file based on its extension."""
    folder_name = FILE_EXTENSIONS.get(file_extension.lower())
    if folder_name:
        if '/' in folder_name:
            # For subfolders (e.g., Downloads/Archives)
            return Path.home() / folder_name
        else:
            # For standard user folders
            return Path.home() / folder_name
    else:
        # Unknown file types go to default folder
        return Path.home() / DEFAULT_FOLDER

def move_file(source_path, file_name):
    """Move file to appropriate folder based on extension."""
    file_path = Path(source_path) / file_name
    file_extension = file_path.suffix
    
    # Skip if no extension
    if not file_extension:
        print(f"  → Skipping {file_name} (no extension)")
        return None
    
    # Get destination folder
    dest_folder = get_destination_folder(file_extension)
    
    # Create destination folder if it doesn't exist
    dest_folder.mkdir(parents=True, exist_ok=True)
    
    # Destination file path
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

def print_organization_rules():
    """Print the current file organization rules."""
    print("\n📋 File Organization Rules:")
    print("=" * 50)
    
    # Group extensions by destination folder
    folder_groups = {}
    for ext, folder in FILE_EXTENSIONS.items():
        if folder not in folder_groups:
            folder_groups[folder] = []
        folder_groups[folder].append(ext)
    
    for folder, extensions in sorted(folder_groups.items()):
        print(f"📁 {folder}:")
        print(f"   {', '.join(sorted(extensions))}")
    
    print(f"📁 {DEFAULT_FOLDER}:")
    print("   All other file types")
    print("=" * 50)

def monitor_downloads_folder():
    """Monitor the Downloads folder for new files and organize them."""
    # Get the Downloads folder path
    downloads_path = Path.home() / "Downloads"
    
    # Check if Downloads folder exists
    if not downloads_path.exists():
        print(f"❌ Downloads folder not found at: {downloads_path}")
        print("Please make sure the Downloads folder exists.")
        return
    
    print(f"🔍 Monitoring Downloads folder: {downloads_path}")
    print("📦 Files will be automatically organized by type.")
    
    # Show organization rules
    print_organization_rules()
    
    print("\n🚀 Starting monitor... Press Ctrl+C to stop.")
    
    # Get initial set of files
    previous_files = set()
    try:
        previous_files = set(os.listdir(downloads_path))
    except OSError as e:
        print(f"❌ Error accessing Downloads folder: {e}")
        return
    
    try:
        while True:
            time.sleep(1)  # Check every second
            
            try:
                # Get current files
                current_files = set(os.listdir(downloads_path))
                
                # Find new files
                new_files = current_files - previous_files
                
                # Process new files
                for file_name in new_files:
                    file_path = downloads_path / file_name
                    if file_path.is_file():  # Only process actual files, not directories
                        print(f"\n📄 New file detected: {file_name}")
                        
                        # Move file to appropriate folder
                        moved_path = move_file(downloads_path, file_name)
                        if moved_path:
                            relative_path = moved_path.relative_to(Path.home())
                            print(f"  ✅ Moved to: ~/{relative_path}")
                        else:
                            print(f"  ❌ Failed to move file")
                
                # Update previous files set
                previous_files = current_files
                
            except OSError as e:
                print(f"❌ Error checking folder: {e}")
                time.sleep(5)  # Wait longer if there's an error
                
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping file monitor...")
    
    print("✨ File monitoring stopped.")

if __name__ == "__main__":
    monitor_downloads_folder()