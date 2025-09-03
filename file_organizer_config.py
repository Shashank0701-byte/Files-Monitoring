# Configuration file for file organization rules
# You can modify these mappings to customize where files are moved

FILE_EXTENSIONS = {
    # Documents
    '.pdf': 'Documents',
    '.doc': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.rtf': 'Documents',
    '.xls': 'Documents',
    '.xlsx': 'Documents',
    '.ppt': 'Documents',
    '.pptx': 'Documents',
    '.odt': 'Documents',
    '.ods': 'Documents',
    '.odp': 'Documents',
    
    # Images
    '.jpg': 'Pictures',
    '.jpeg': 'Pictures',
    '.png': 'Pictures',
    '.gif': 'Pictures',
    '.bmp': 'Pictures',
    '.tiff': 'Pictures',
    '.svg': 'Pictures',
    '.webp': 'Pictures',
    '.ico': 'Pictures',
    '.raw': 'Pictures',
    
    # Videos
    '.mp4': 'Videos',
    '.avi': 'Videos',
    '.mkv': 'Videos',
    '.mov': 'Videos',
    '.wmv': 'Videos',
    '.flv': 'Videos',
    '.webm': 'Videos',
    '.m4v': 'Videos',
    '.mpg': 'Videos',
    '.mpeg': 'Videos',
    
    # Audio
    '.mp3': 'Music',
    '.wav': 'Music',
    '.flac': 'Music',
    '.aac': 'Music',
    '.ogg': 'Music',
    '.wma': 'Music',
    '.m4a': 'Music',
    '.opus': 'Music',
    
    # Archives
    '.zip': 'Downloads/Archives',
    '.rar': 'Downloads/Archives',
    '.7z': 'Downloads/Archives',
    '.tar': 'Downloads/Archives',
    '.gz': 'Downloads/Archives',
    '.bz2': 'Downloads/Archives',
    '.xz': 'Downloads/Archives',
    
    # Executables and Installers
    '.exe': 'Downloads/Software',
    '.msi': 'Downloads/Software',
    '.deb': 'Downloads/Software',
    '.dmg': 'Downloads/Software',
    '.pkg': 'Downloads/Software',
    '.appx': 'Downloads/Software',
    
    # Code files
    '.py': 'Documents/Code',
    '.js': 'Documents/Code',
    '.html': 'Documents/Code',
    '.css': 'Documents/Code',
    '.java': 'Documents/Code',
    '.cpp': 'Documents/Code',
    '.c': 'Documents/Code',
    '.php': 'Documents/Code',
    '.rb': 'Documents/Code',
    '.go': 'Documents/Code',
    '.rs': 'Documents/Code',
    '.ts': 'Documents/Code',
    '.json': 'Documents/Code',
    '.xml': 'Documents/Code',
    '.yml': 'Documents/Code',
    '.yaml': 'Documents/Code',
    
    # E-books
    '.epub': 'Documents/Books',
    '.mobi': 'Documents/Books',
    '.azw': 'Documents/Books',
    '.azw3': 'Documents/Books',
    
    # Fonts
    '.ttf': 'Downloads/Fonts',
    '.otf': 'Downloads/Fonts',
    '.woff': 'Downloads/Fonts',
    '.woff2': 'Downloads/Fonts'
}

# Default folder for unknown file types
DEFAULT_FOLDER = 'Downloads/Others'