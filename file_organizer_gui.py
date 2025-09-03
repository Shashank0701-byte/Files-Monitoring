import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from pathlib import Path

class FileOrganizerGUI:
    """GUI for managing file organization rules."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer - Rule Manager")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configuration file path
        self.config_file = Path("file_rules.json")
        
        # Data storage
        self.file_extensions = {}
        self.settings = {}
        
        # Create GUI
        self.create_widgets()
        self.load_configuration()
        self.refresh_rules_display()
        
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="File Organization Rules Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Rules list
        left_frame = ttk.LabelFrame(main_frame, text="Current Rules", padding="5")
        left_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Treeview for rules
        columns = ("Extension", "Destination Folder")
        self.rules_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        self.rules_tree.heading("Extension", text="File Extension")
        self.rules_tree.heading("Destination Folder", text="Destination Folder")
        self.rules_tree.column("Extension", width=150)
        self.rules_tree.column("Destination Folder", width=300)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.rules_tree.yview)
        self.rules_tree.configure(yscrollcommand=scrollbar.set)
        
        self.rules_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Right panel - Controls
        right_frame = ttk.LabelFrame(main_frame, text="Rule Management", padding="5")
        right_frame.grid(row=1, column=2, sticky="nsew")
        
        # Add rule section
        ttk.Label(right_frame, text="Add/Edit Rule:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(right_frame, text="File Extension:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.ext_entry = ttk.Entry(right_frame, width=15)
        self.ext_entry.grid(row=1, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Destination:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.dest_entry = ttk.Entry(right_frame, width=20)
        self.dest_entry.grid(row=2, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.add_btn = ttk.Button(btn_frame, text="Add Rule", command=self.add_rule)
        self.add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.update_btn = ttk.Button(btn_frame, text="Update Rule", command=self.update_rule, state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete Rule", command=self.delete_rule, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky="ew", pady=20)
        
        # Quick add section
        ttk.Label(right_frame, text="Quick Add:", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        quick_buttons = [
            ("Documents", "Documents"),
            ("Pictures", "Pictures"),
            ("Videos", "Videos"),
            ("Music", "Music"),
            ("Archives", "Downloads/Archives"),
            ("Software", "Downloads/Software")
        ]
        
        for i, (text, folder) in enumerate(quick_buttons):
            btn = ttk.Button(right_frame, text=text, 
                           command=lambda f=folder: self.quick_add_destination(f))
            btn.grid(row=6 + i//2, column=i%2, sticky="ew", pady=2, padx=2)
        
        # Separator
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).grid(row=9, column=0, columnspan=2, sticky="ew", pady=20)
        
        # File operations
        ttk.Label(right_frame, text="File Operations:", font=("Arial", 10, "bold")).grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        file_btn_frame = ttk.Frame(right_frame)
        file_btn_frame.grid(row=11, column=0, columnspan=2, sticky="ew")
        
        ttk.Button(file_btn_frame, text="Load Config", command=self.load_config_file).pack(side=tk.TOP, fill=tk.X, pady=2)
        ttk.Button(file_btn_frame, text="Save Config", command=self.save_configuration).pack(side=tk.TOP, fill=tk.X, pady=2)
        ttk.Button(file_btn_frame, text="Import Config", command=self.import_config).pack(side=tk.TOP, fill=tk.X, pady=2)
        ttk.Button(file_btn_frame, text="Export Config", command=self.export_config).pack(side=tk.TOP, fill=tk.X, pady=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        # Bind events
        self.rules_tree.bind("<<TreeviewSelect>>", self.on_rule_select)
        self.ext_entry.bind("<KeyRelease>", self.on_entry_change)
        self.dest_entry.bind("<KeyRelease>", self.on_entry_change)
        
        # Configure column weights
        right_frame.columnconfigure(1, weight=1)
        
    def load_configuration(self):
        """Load configuration from JSON file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Flatten the nested file_extensions structure
                self.file_extensions = {}
                for category, extensions in config.get("file_extensions", {}).items():
                    if isinstance(extensions, dict) and not category.startswith("_"):
                        self.file_extensions.update(extensions)
                
                self.settings = config.get("settings", {})
                self.status_var.set(f"Loaded {len(self.file_extensions)} rules from {self.config_file}")
            else:
                self.create_default_config()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration."""
        self.file_extensions = {
            ".pdf": "Documents",
            ".jpg": "Pictures",
            ".png": "Pictures",
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
        self.status_var.set("Created default configuration")
    
    def refresh_rules_display(self):
        """Refresh the rules display in the treeview."""
        # Clear existing items
        for item in self.rules_tree.get_children():
            self.rules_tree.delete(item)
        
        # Add current rules
        for ext, folder in sorted(self.file_extensions.items()):
            self.rules_tree.insert("", tk.END, values=(ext, folder))
        
        self.status_var.set(f"Displaying {len(self.file_extensions)} rules")
    
    def on_rule_select(self, event):
        """Handle rule selection in treeview."""
        selection = self.rules_tree.selection()
        if selection:
            item = self.rules_tree.item(selection[0])
            ext, folder = item['values']
            
            self.ext_entry.delete(0, tk.END)
            self.ext_entry.insert(0, ext)
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)
            
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            self.add_btn.config(text="Add Rule")
        else:
            self.update_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
    
    def on_entry_change(self, event):
        """Handle changes in entry fields."""
        ext = self.ext_entry.get().strip()
        dest = self.dest_entry.get().strip()
        
        if ext and dest:
            if ext in self.file_extensions:
                self.add_btn.config(text="Update Rule")
            else:
                self.add_btn.config(text="Add Rule")
    
    def add_rule(self):
        """Add or update a rule."""
        ext = self.ext_entry.get().strip()
        dest = self.dest_entry.get().strip()
        
        if not ext or not dest:
            messagebox.showwarning("Warning", "Please enter both extension and destination")
            return
        
        # Ensure extension starts with dot
        if not ext.startswith('.'):
            ext = '.' + ext
        
        # Validate extension format
        if not ext.replace('.', '').replace('_', '').replace('-', '').isalnum():
            messagebox.showwarning("Warning", "Invalid extension format")
            return
        
        self.file_extensions[ext] = dest
        self.refresh_rules_display()
        
        # Clear entries
        self.ext_entry.delete(0, tk.END)
        self.dest_entry.delete(0, tk.END)
        
        self.status_var.set(f"Added/Updated rule: {ext} → {dest}")
    
    def update_rule(self):
        """Update the selected rule."""
        self.add_rule()
    
    def delete_rule(self):
        """Delete the selected rule."""
        selection = self.rules_tree.selection()
        if not selection:
            return
        
        item = self.rules_tree.item(selection[0])
        ext = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Delete rule for {ext}?"):
            del self.file_extensions[ext]
            self.refresh_rules_display()
            
            # Clear entries and disable buttons
            self.ext_entry.delete(0, tk.END)
            self.dest_entry.delete(0, tk.END)
            self.update_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
            
            self.status_var.set(f"Deleted rule for {ext}")
    
    def quick_add_destination(self, folder):
        """Quick add destination folder to entry."""
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, folder)
        self.ext_entry.focus()
    
    def save_configuration(self):
        """Save current configuration to JSON file."""
        try:
            # Organize extensions by category for better JSON structure
            organized_config = {
                "file_extensions": {
                    "_comment": "Define where files should be moved based on their extensions",
                    "_format": "extension: destination_folder",
                    "_paths": "Use relative paths from user home directory"
                },
                "settings": self.settings
            }
            
            # Group extensions by destination for better organization
            destinations = {}
            for ext, dest in self.file_extensions.items():
                if dest not in destinations:
                    destinations[dest] = {}
                destinations[dest][ext] = dest
            
            # Add grouped extensions to config
            category_names = {
                "Documents": "documents",
                "Pictures": "images", 
                "Videos": "videos",
                "Music": "audio",
                "Downloads/Archives": "archives",
                "Downloads/Software": "software",
                "Documents/Code": "code",
                "Documents/Books": "books",
                "Downloads/Fonts": "fonts"
            }
            
            for dest, extensions in destinations.items():
                category = category_names.get(dest, dest.replace("/", "_").lower())
                organized_config["file_extensions"][category] = {ext: dest for ext in extensions}
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(organized_config, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Configuration saved to {self.config_file}")
            self.status_var.set(f"Saved {len(self.file_extensions)} rules to {self.config_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def load_config_file(self):
        """Reload configuration from file."""
        self.load_configuration()
        self.refresh_rules_display()
    
    def import_config(self):
        """Import configuration from another JSON file."""
        file_path = filedialog.askopenfilename(
            title="Import Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Flatten the nested file_extensions structure
                imported_extensions = {}
                for category, extensions in config.get("file_extensions", {}).items():
                    if isinstance(extensions, dict) and not category.startswith("_"):
                        imported_extensions.update(extensions)
                
                if messagebox.askyesno("Import Configuration", 
                                     f"Import {len(imported_extensions)} rules?\nThis will replace current rules."):
                    self.file_extensions = imported_extensions
                    self.settings.update(config.get("settings", {}))
                    self.refresh_rules_display()
                    self.status_var.set(f"Imported {len(imported_extensions)} rules from {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import configuration: {e}")
    
    def export_config(self):
        """Export current configuration to a JSON file."""
        file_path = filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                config = {
                    "file_extensions": {
                        "rules": self.file_extensions
                    },
                    "settings": self.settings
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Configuration exported to {file_path}")
                self.status_var.set(f"Exported configuration to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export configuration: {e}")

def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()