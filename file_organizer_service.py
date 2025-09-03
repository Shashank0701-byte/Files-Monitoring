"""
File Organizer Service
A Windows service wrapper for the file organization monitor.
"""

import os
import sys
import time
import logging
from pathlib import Path
import win32serviceutil
import win32service
import win32event
import servicemanager

# Add the script directory to path to import our modules
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from folder_monitor_json import monitor_downloads_folder, FileOrganizerConfig

class FileOrganizerService(win32serviceutil.ServiceFramework):
    """Windows service for file organization monitoring."""
    
    _svc_name_ = "FileOrganizerService"
    _svc_display_name_ = "File Organizer Monitor Service"
    _svc_description_ = "Automatically organizes files in the Downloads folder based on JSON rules"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for the service."""
        log_dir = Path.home() / "AppData" / "Local" / "FileOrganizer"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / "service.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def SvcStop(self):
        """Stop the service."""
        self.logger.info("File Organizer Service stopping...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
    
    def SvcDoRun(self):
        """Main service execution."""
        self.logger.info("File Organizer Service starting...")
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        try:
            self.main_loop()
        except Exception as e:
            self.logger.error(f"Service error: {e}")
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_ERROR_TYPE,
                servicemanager.PYS_SERVICE_STOPPED,
                (self._svc_name_, str(e))
            )
    
    def main_loop(self):
        """Main monitoring loop."""
        # Load configuration
        config = FileOrganizerConfig()
        
        # Get the Downloads folder path
        downloads_path = Path.home() / "Downloads"
        
        if not downloads_path.exists():
            self.logger.error(f"Downloads folder not found: {downloads_path}")
            return
        
        self.logger.info(f"Monitoring Downloads folder: {downloads_path}")
        self.logger.info(f"Loaded {len(config.file_extensions)} file organization rules")
        
        # Get initial set of files
        previous_files = set()
        try:
            previous_files = set(os.listdir(downloads_path))
        except OSError as e:
            self.logger.error(f"Error accessing Downloads folder: {e}")
            return
        
        last_config_check = time.time()
        config_check_interval = 5  # Check for config changes every 5 seconds
        
        while self.is_alive:
            try:
                # Check if service should stop
                if win32event.WaitForSingleObject(self.hWaitStop, 0) == win32event.WAIT_OBJECT_0:
                    break
                
                check_interval = config.settings.get('check_interval_seconds', 1)
                time.sleep(check_interval)
                
                # Check if config file has been modified
                current_time = time.time()
                if current_time - last_config_check > config_check_interval:
                    if config.config_file.exists():
                        file_mtime = config.config_file.stat().st_mtime
                        if file_mtime > last_config_check:
                            self.logger.info("Reloading configuration...")
                            config.reload_config()
                    last_config_check = current_time
                
                # Get current files
                current_files = set(os.listdir(downloads_path))
                
                # Find new files
                new_files = current_files - previous_files
                
                # Process new files
                for file_name in new_files:
                    file_path = downloads_path / file_name
                    if file_path.is_file():  # Only process actual files
                        self.logger.info(f"New file detected: {file_name}")
                        
                        # Move file to appropriate folder
                        moved_path = self.move_file(downloads_path, file_name, config)
                        if moved_path:
                            relative_path = moved_path.relative_to(Path.home())
                            self.logger.info(f"Moved to: ~/{relative_path}")
                        else:
                            self.logger.warning(f"Failed to move file: {file_name}")
                
                # Update previous files set
                previous_files = current_files
                
            except OSError as e:
                self.logger.error(f"Error checking folder: {e}")
                time.sleep(5)  # Wait longer if there's an error
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                time.sleep(1)
        
        self.logger.info("File Organizer Service stopped")
    
    def move_file(self, source_path, file_name, config):
        """Move file to appropriate folder based on extension and configuration."""
        import shutil
        
        file_path = Path(source_path) / file_name
        file_extension = file_path.suffix
        
        # Skip if no extension
        if not file_extension:
            self.logger.debug(f"Skipping {file_name} (no extension)")
            return None
        
        # Get destination folder from config
        dest_folder = config.get_destination_folder(file_extension)
        
        # Create destination folder if enabled in settings
        if config.settings.get("create_folders", True):
            dest_folder.mkdir(parents=True, exist_ok=True)
        elif not dest_folder.exists():
            self.logger.warning(f"Destination folder doesn't exist: {dest_folder}")
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
            self.logger.warning(f"File already exists: {dest_path}")
            return None
        
        try:
            shutil.move(str(file_path), str(dest_path))
            return dest_path
        except Exception as e:
            self.logger.error(f"Error moving file {file_name}: {e}")
            return None

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FileOrganizerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FileOrganizerService)