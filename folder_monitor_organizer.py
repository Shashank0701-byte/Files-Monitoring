import os
import time
import shutil
import logging
from pathlib import Path
from datetime import datetime
from file_organizer_config import FILE_EXTENSIONS, DEFAULT_FOLDER

def setup_logging():
    """Setup logging for the file organizer."""
    # Create log directory
    log_dir = Path.home() / "AppData" / "Local" / "FileOrganizer"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup logger
    logger = logging.getLogger('FileOrganizerEnhanced')
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # File handler
    log_file = log_dir / "file_organizer_enhanced.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

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

def move_file(source_path, file_name, logger):
    """Move file to appropriate folder based on extension."""
    file_path = Path(source_path) / file_name
    file_extension = file_path.suffix
    
    # Skip if no extension
    if not file_extension:
        logger.debug(f"Skipping {file_name} (no extension)")
        return None
    
    # Get destination folder
    dest_folder = get_destination_folder(file_extension)
    
    # Log the intended move
    logger.info(f"Processing file: {file_name} ({file_extension}) → {dest_folder.name}")
    
    # Create destination folder if it doesn't exist
    if not dest_folder.exists():
        logger.info(f"Creating destination folder: {dest_folder}")
        dest_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created folder: {dest_folder}")
    
    # Destination file path
    dest_path = dest_folder / file_name
    original_dest_path = dest_path
    
    # Handle file name conflicts
    counter = 1
    while dest_path.exists():
        name_part = original_dest_path.stem
        ext_part = original_dest_path.suffix
        new_name = f"{name_part}_{counter}{ext_part}"
        dest_path = dest_folder / new_name
        counter += 1
        
    if dest_path != original_dest_path:
        logger.info(f"File renamed to avoid conflict: {file_name} → {dest_path.name}")
    
    # Get file size for logging
    try:
        file_size = file_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
    except:
        file_size_mb = 0
    
    # Attempt to move the file
    try:
        start_time = time.time()
        shutil.move(str(file_path), str(dest_path))
        move_time = time.time() - start_time
        
        logger.info(f"✅ FILE MOVED: {file_name} → {dest_path}")
        logger.info(f"   Size: {file_size_mb:.2f} MB, Time: {move_time:.2f}s")
        
        return dest_path
        
    except PermissionError as e:
        logger.error(f"❌ Permission denied moving {file_name}: {e}")
        return None
    except FileNotFoundError as e:
        logger.error(f"❌ File not found when moving {file_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Error moving file {file_name}: {e}")
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
    # Setup logging
    logger = setup_logging()
    
    # Log startup information
    logger.info("="*60)
    logger.info("FILE ORGANIZER ENHANCED STARTED")
    logger.info(f"Version: Enhanced with built-in rules")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*60)
    
    # Get the Downloads folder path
    downloads_path = Path.home() / "Downloads"
    
    # Check if Downloads folder exists
    if not downloads_path.exists():
        logger.error(f"Downloads folder not found at: {downloads_path}")
        logger.error("Please make sure the Downloads folder exists.")
        return
    
    logger.info(f"Monitoring Downloads folder: {downloads_path}")
    logger.info("Files will be automatically organized by type.")
    
    # Show organization rules
    print_organization_rules()
    
    print("\n🚀 Starting monitor... Press Ctrl+C to stop.")
    
    # Get initial set of files
    previous_files = set()
    try:
        previous_files = set(os.listdir(downloads_path))
        logger.info(f"Initial scan found {len(previous_files)} files in Downloads folder")
    except OSError as e:
        logger.error(f"Error accessing Downloads folder: {e}")
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
                        logger.info(f"📄 NEW FILE DETECTED: {file_name}")
                        print(f"\n📄 New file detected: {file_name}")
                        
                        # Move file to appropriate folder
                        moved_path = move_file(downloads_path, file_name, logger)
                        if moved_path:
                            relative_path = moved_path.relative_to(Path.home())
                            print(f"  ✅ Moved to: ~/{relative_path}")
                            logger.info(f"File successfully organized: {file_name} → ~/{relative_path}")
                        else:
                            print(f"  ❌ Failed to move file")
                            logger.error(f"Failed to organize file: {file_name}")
                
                # Update previous files set
                previous_files = current_files
                
            except OSError as e:
                logger.error(f"Error checking folder: {e}")
                print(f"❌ Error checking folder: {e}")
                time.sleep(5)  # Wait longer if there's an error
                
    except KeyboardInterrupt:
        logger.info("File monitor stopped by user (Ctrl+C)")
        print("\n\n🛑 Stopping file monitor...")
    except Exception as e:
        logger.error(f"Unexpected error in monitor loop: {e}")
        print(f"\n\n❌ Unexpected error: {e}")
    
    logger.info("File monitoring session ended")
    logger.info("="*60)
    print("✨ File monitoring stopped.")

if __name__ == "__main__":
    monitor_downloads_folder()