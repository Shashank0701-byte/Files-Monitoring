# Folder Monitor & File Organizer

A Python script that continuously monitors the Downloads folder and automatically organizes files by moving them to appropriate folders based on their extensions.

## Features

🔍 **Real-time monitoring** - Continuously watches the Downloads folder for new files  
📦 **Automatic organization** - Moves files to appropriate folders based on file extensions  
🛠️ **Customizable rules** - Easy to modify file organization rules  
⚡ **No external dependencies** - Uses only Python standard library  
🔒 **Safe operation** - Handles file name conflicts and errors gracefully  

## Files

- **[folder_monitor_simple.py](folder_monitor_simple.py)** - Basic version with built-in organization rules
- **[folder_monitor_organizer.py](folder_monitor_organizer.py)** - Enhanced version with configurable rules
- **[file_organizer_config.py](file_organizer_config.py)** - Configuration file for customizing organization rules
- **[folder_monitor.py](folder_monitor.py)** - Original version using watchdog library
- **[requirements.txt](requirements.txt)** - Dependencies for watchdog version

## File Organization Rules

### Documents → `~/Documents`
- PDF files (.pdf)
- Microsoft Office (.doc, .docx, .xls, .xlsx, .ppt, .pptx)
- Text files (.txt, .rtf)
- LibreOffice (.odt, .ods, .odp)

### Pictures → `~/Pictures`
- Images (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp, .ico, .raw)

### Videos → `~/Videos`
- Video files (.mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpg, .mpeg)

### Music → `~/Music`
- Audio files (.mp3, .wav, .flac, .aac, .ogg, .wma, .m4a, .opus)

### Special Downloads Subfolders
- **Archives** → `~/Downloads/Archives` (.zip, .rar, .7z, .tar, .gz, .bz2, .xz)
- **Software** → `~/Downloads/Software` (.exe, .msi, .deb, .dmg, .pkg, .appx)
- **Code** → `~/Documents/Code` (.py, .js, .html, .css, .java, .cpp, .c, .php, .rb, .go, .rs, .ts, .json, .xml, .yml, .yaml)
- **Books** → `~/Documents/Books` (.epub, .mobi, .azw, .azw3)
- **Fonts** → `~/Downloads/Fonts` (.ttf, .otf, .woff, .woff2)
- **Others** → `~/Downloads/Others` (unknown file types)

## Usage

### Quick Start (Recommended)
```bash
python folder_monitor_organizer.py
```

### Basic Version
```bash
python folder_monitor_simple.py
```

### With Watchdog Library
```bash
pip install -r requirements.txt
python folder_monitor.py
```

## Customization

To customize file organization rules, edit the `file_organizer_config.py` file:

```python
FILE_EXTENSIONS = {
    '.pdf': 'Documents',           # Move PDFs to Documents folder
    '.jpg': 'Pictures',            # Move images to Pictures folder
    '.mp4': 'Videos',              # Move videos to Videos folder
    '.zip': 'Downloads/Archives',  # Create subfolder in Downloads
    # Add your own rules...
}
```

## Safety Features

- **Conflict handling** - If a file with the same name exists, adds a number suffix (e.g., `file_1.pdf`)
- **Error handling** - Continues monitoring even if individual file moves fail
- **Folder creation** - Automatically creates destination folders if they don't exist
- **File validation** - Only processes actual files, ignores directories

## Requirements

- Python 3.6 or higher
- No external dependencies for the main functionality
- Optional: `watchdog` library for the advanced monitoring version

## Stopping the Monitor

Press `Ctrl+C` to stop the file monitor at any time.

## Example Output

```
🔍 Monitoring Downloads folder: C:\Users\username\Downloads
📦 Files will be automatically organized by type.

📋 File Organization Rules:
==================================================
📁 Documents:
   .doc, .docx, .pdf, .ppt, .pptx, .txt, .xls, .xlsx
📁 Pictures:
   .bmp, .gif, .jpg, .jpeg, .png, .svg, .tiff, .webp
📁 Videos:
   .avi, .mkv, .mov, .mp4, .webm, .wmv
==================================================

🚀 Starting monitor... Press Ctrl+C to stop.

📄 New file detected: document.pdf
  ✅ Moved to: ~/Documents/document.pdf

📄 New file detected: photo.jpg
  ✅ Moved to: ~/Pictures/photo.jpg
```