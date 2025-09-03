"""
Startup File Organizer
A lightweight startup script that runs the file organizer on system startup.
Alternative to Windows service for simpler installation.
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
import winreg

def setup_logging():
    """Setup logging for the startup script."""
    log_dir = Path.home() / "AppData" / "Local" / "FileOrganizer"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "startup.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler() if "--debug" in sys.argv else logging.NullHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def add_to_startup():
    """Add the startup script to Windows registry for auto-start."""
    try:
        script_path = Path(__file__).absolute()
        python_exe = sys.executable
        
        # Command to run this script on startup
        command = f'"{python_exe}" "{script_path}" --startup'
        
        # Add to registry
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.SetValueEx(key, "FileOrganizer", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        print("✅ File Organizer added to startup successfully!")
        print(f"Command: {command}")
        return True
        
    except Exception as e:
        print(f"❌ Error adding to startup: {e}")
        return False

def remove_from_startup():
    """Remove the startup script from Windows registry."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.DeleteValue(key, "FileOrganizer")
        winreg.CloseKey(key)
        
        print("✅ File Organizer removed from startup successfully!")
        return True
        
    except FileNotFoundError:
        print("ℹ️ File Organizer was not in startup registry")
        return True
    except Exception as e:
        print(f"❌ Error removing from startup: {e}")
        return False

def check_startup_status():
    """Check if the script is in startup registry."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        
        value, _ = winreg.QueryValueEx(key, "FileOrganizer")
        winreg.CloseKey(key)
        
        print("✅ File Organizer is currently in startup")
        print(f"Command: {value}")
        return True
        
    except FileNotFoundError:
        print("❌ File Organizer is not in startup")
        return False
    except Exception as e:
        print(f"❌ Error checking startup status: {e}")
        return False

def run_file_organizer():
    """Run the file organizer monitor."""
    logger = setup_logging()
    logger.info("Starting File Organizer from startup...")
    
    try:
        # Change to script directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Check if JSON monitor exists
        json_monitor = script_dir / "folder_monitor_json.py"
        if json_monitor.exists():
            logger.info("Running JSON-based file monitor...")
            # Import and run the monitor
            sys.path.insert(0, str(script_dir))
            from folder_monitor_json import monitor_downloads_folder
            monitor_downloads_folder()
        else:
            logger.error("folder_monitor_json.py not found!")
            
    except KeyboardInterrupt:
        logger.info("File Organizer stopped by user")
    except Exception as e:
        logger.error(f"Error running file organizer: {e}")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("File Organizer Startup Manager")
        print("=" * 40)
        print("Usage:")
        print("  python startup_organizer.py install   - Add to startup")
        print("  python startup_organizer.py uninstall - Remove from startup") 
        print("  python startup_organizer.py status    - Check startup status")
        print("  python startup_organizer.py run       - Run file organizer now")
        return
    
    command = sys.argv[1].lower()
    
    if command == "install":
        add_to_startup()
    elif command == "uninstall":
        remove_from_startup()
    elif command == "status":
        check_startup_status()
    elif command == "run":
        run_file_organizer()
    elif command == "--startup":
        # This is called from Windows startup
        run_file_organizer()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()