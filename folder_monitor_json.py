import os
import time
import shutil
import json
from pathlib import Path

class FileOrganizerConfig:
    """Handle loading and managing file organization configuration from JSON."""
    
    def __init__(self, config_file="file_rules.json"):
        self.config_file = Path(config_file)
        self.file_extensions = {}
        self.settings = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file."""
        if not self.config_file.exists():
            print(f"❌ Configuration file not found: {self.config_file}")
            print("Creating default configuration file...")
            self.create_default_config()
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Flatten the nested file_extensions structure
            self.file_extensions = {}
            for category, extensions in config.get("file_extensions", {}).items():
                if isinstance(extensions, dict) and not category.startswith("_"):
                    self.file_extensions.update(extensions)
            
            self.settings = config.get("settings", {})
            
            print(f"✅ Loaded configuration from {self.config_file}")
            print(f"📊 Monitoring {len(self.file_extensions)} file types")
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON config: {e}")
            print("Using default configuration...")
            self.create_default_config()
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            print("Using default configuration...")
            self.create_default_config()
    
    def create_default_config(self):
        """Create a default configuration."""
        self.file_extensions = {
            ".pdf": "Documents",
            ".jpg": "Pictures",
            ".mp3": "Music",
            ".mp4": "Videos",
            ".zip": "Downloads/Archives"
        }
        self.settings = {
            "default_folder": "Downloads/Others",
            "check_interval_seconds": 1,
            "handle_duplicates": True,
            "create_folders": True,
            "case_sensitive": False
        }
    
    def get_destination_folder(self, file_extension):
        """Get the destination folder for a file based on its extension."""
        # Handle case sensitivity setting
        ext_key = file_extension.lower() if not self.settings.get("case_sensitive", False) else file_extension
        
        folder_name = self.file_extensions.get(ext_key)
        if folder_name:
            return Path.home() / folder_name
        else:
            default_folder = self.settings.get("default_folder", "Downloads/Others")
            return Path.home() / default_folder
    
    def reload_config(self):
        """Reload configuration from file."""
        print("🔄 Reloading configuration...")
        self.load_config()

def move_file(source_path, file_name, config):
    """Move file to appropriate folder based on extension and configuration."""
    file_path = Path(source_path) / file_name
    file_extension = file_path.suffix
    
    # Skip if no extension
    if not file_extension:
        print(f"  → Skipping {file_name} (no extension)")
        return None
    
    # Get destination folder from config
    dest_folder = config.get_destination_folder(file_extension)
    
    # Create destination folder if enabled in settings
    if config.settings.get("create_folders", True):
        dest_folder.mkdir(parents=True, exist_ok=True)
    elif not dest_folder.exists():
        print(f"  → Destination folder doesn't exist: {dest_folder}")
        return None
    
    # Destination file path
    dest_path = dest_folder / file_name
    
    # Handle file name conflicts if enabled
    if config.settings.get("handle_duplicates", True):
        counter = 1
        original_dest_path = dest_path
        while dest_path.exists():
            name_part = original_dest_path.stem
            ext_part = original_dest_path.suffix
            dest_path = dest_folder / f"{name_part}_{counter}{ext_part}"
            counter += 1
    elif dest_path.exists():
        print(f"  → File already exists: {dest_path}")
        return None
    
    try:
        shutil.move(str(file_path), str(dest_path))
        return dest_path
    except Exception as e:
        print(f"  → Error moving file {file_name}: {e}")
        return None

def print_organization_rules(config):
    """Print the current file organization rules from config."""
    print("\n📋 File Organization Rules (from JSON config):")
    print("=" * 60)
    
    # Group extensions by destination folder
    folder_groups = {}
    for ext, folder in config.file_extensions.items():
        if folder not in folder_groups:
            folder_groups[folder] = []
        folder_groups[folder].append(ext)
    
    for folder, extensions in sorted(folder_groups.items()):
        print(f"📁 {folder}:")
        print(f"   {', '.join(sorted(extensions))}")
    
    default_folder = config.settings.get("default_folder", "Downloads/Others")
    print(f"📁 {default_folder}:")
    print("   All other file types")
    print("=" * 60)
    
    # Print settings
    print("\n⚙️  Settings:")
    for key, value in config.settings.items():
        print(f"   {key}: {value}")
    print("=" * 60)

def monitor_downloads_folder():
    """Monitor the Downloads folder for new files and organize them using JSON config."""
    # Load configuration
    config = FileOrganizerConfig()
    
    # Get the Downloads folder path
    downloads_path = Path.home() / "Downloads"
    
    # Check if Downloads folder exists
    if not downloads_path.exists():
        print(f"❌ Downloads folder not found at: {downloads_path}")
        print("Please make sure the Downloads folder exists.")
        return
    
    print(f"🔍 Monitoring Downloads folder: {downloads_path}")
    print("📦 Files will be automatically organized based on JSON rules.")
    print("💡 Edit 'file_rules.json' to customize organization rules.")
    
    # Show organization rules
    print_organization_rules(config)
    
    print(f"\n🚀 Starting monitor (checking every {config.settings.get('check_interval_seconds', 1)}s)...")
    print("Press Ctrl+C to stop, or modify file_rules.json to update rules.")
    
    # Get initial set of files
    previous_files = set()
    try:
        previous_files = set(os.listdir(downloads_path))
    except OSError as e:
        print(f"❌ Error accessing Downloads folder: {e}")
        return
    
    last_config_check = time.time()
    config_check_interval = 5  # Check for config changes every 5 seconds
    
    try:
        while True:
            check_interval = config.settings.get('check_interval_seconds', 1)
            time.sleep(check_interval)
            
            # Check if config file has been modified
            current_time = time.time()
            if current_time - last_config_check > config_check_interval:
                if config.config_file.exists():
                    file_mtime = config.config_file.stat().st_mtime
                    if file_mtime > last_config_check:
                        config.reload_config()
                        print_organization_rules(config)
                last_config_check = current_time
            
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
                        moved_path = move_file(downloads_path, file_name, config)
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