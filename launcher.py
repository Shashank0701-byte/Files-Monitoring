#!/usr/bin/env python3
"""
File Organizer Launcher
Provides options to run the GUI rule manager or the file monitor.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from pathlib import Path

class LauncherGUI:
    """Simple launcher for File Organizer tools."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer Launcher")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the launcher GUI."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="File Organizer Tools", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Description
        desc_text = ("Choose which tool to launch:\n\n"
                    "• Rule Manager: Add/edit/delete file organization rules\n"
                    "• File Monitor: Start monitoring Downloads folder\n"
                    "• Monitor (Simple): Basic version without JSON config")\n        
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.LEFT)
        desc_label.grid(row=1, column=0, pady=(0, 20))
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, pady=10)
        
        # Buttons
        gui_btn = ttk.Button(btn_frame, text="📋 Rule Manager (GUI)", 
                            command=self.launch_gui, width=25)
        gui_btn.grid(row=0, column=0, pady=5)
        
        monitor_btn = ttk.Button(btn_frame, text="🔍 File Monitor (JSON)", 
                               command=self.launch_monitor, width=25)
        monitor_btn.grid(row=1, column=0, pady=5)
        
        simple_btn = ttk.Button(btn_frame, text="📁 File Monitor (Simple)", 
                               command=self.launch_simple, width=25)
        simple_btn.grid(row=2, column=0, pady=5)
        
        organizer_btn = ttk.Button(btn_frame, text="⚙️ File Monitor (Enhanced)", 
                                  command=self.launch_organizer, width=25)
        organizer_btn.grid(row=3, column=0, pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=3, column=0, sticky="ew", pady=20)
        
        # Exit button
        exit_btn = ttk.Button(main_frame, text="Exit", command=self.root.quit)
        exit_btn.grid(row=4, column=0, pady=10)
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select a tool to launch")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=("Arial", 9), foreground="gray")
        status_label.grid(row=5, column=0, pady=(10, 0))
        
    def launch_gui(self):
        """Launch the rule manager GUI."""
        try:
            subprocess.Popen([sys.executable, "file_organizer_gui.py"])
            self.status_var.set("Launched Rule Manager GUI")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch GUI: {e}")
    
    def launch_monitor(self):
        """Launch the JSON-based file monitor."""
        try:
            subprocess.Popen([sys.executable, "folder_monitor_json.py"])
            self.status_var.set("Launched JSON File Monitor")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch monitor: {e}")
    
    def launch_simple(self):
        """Launch the simple file monitor."""
        try:
            subprocess.Popen([sys.executable, "folder_monitor_simple.py"])
            self.status_var.set("Launched Simple File Monitor")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch simple monitor: {e}")
    
    def launch_organizer(self):
        """Launch the enhanced file organizer."""
        try:
            subprocess.Popen([sys.executable, "folder_monitor_organizer.py"])
            self.status_var.set("Launched Enhanced File Monitor")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch organizer: {e}")

def main():
    """Main function."""
    root = tk.Tk()
    app = LauncherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()