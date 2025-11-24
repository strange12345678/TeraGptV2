import os
import time
from datetime import datetime
import logging

log = logging.getLogger("TeraBoxBot")

def auto_rename_file(filename: str, pattern: str = "timestamp", variables: dict = None) -> str:
    """
    Auto-rename a file based on the specified pattern.
    
    Args:
        filename: Original filename
        pattern: Rename pattern - "timestamp", "datetime", or custom pattern with variables
        variables: Dict of variables for custom patterns (e.g., {file_name}, {file_size}, {username})
    
    Returns:
        New filename with pattern applied
    """
    try:
        name, ext = os.path.splitext(filename)
        
        if pattern == "timestamp":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{name}_{timestamp}{ext}"
            log.info(f"Auto-renamed: {filename} -> {new_name}")
            return new_name
        
        elif pattern == "datetime":
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_name = f"{name}_{timestamp}{ext}"
            log.info(f"Auto-renamed: {filename} -> {new_name}")
            return new_name
        
        elif pattern and "{" in pattern:
            # Custom pattern with variables
            if not variables:
                variables = {}
            
            # Set default variables including date/time formats
            now = datetime.now()
            defaults = {
                "file_name": filename,  # Original filename with extension
                "file_size": variables.get("file_size", "unknown"),
                "date": now.strftime("%Y-%m-%d"),
                "timestamp": now.strftime("%Y%m%d_%H%M%S"),
                "time": now.strftime("%H-%M-%S"),
                "datetime": now.strftime("%Y-%m-%d_%H-%M-%S"),
            }
            defaults.update(variables)
            
            try:
                # Replace variables in pattern
                # Note: {file_name} already includes extension, so don't add it again
                new_name = pattern.format(**defaults)
                
                # Sanitize filename - remove only filesystem-dangerous characters
                # Allow everything except: / \ : * ? " < > |
                dangerous_chars = '/\\:*?"<>|'
                new_name = "".join(c for c in new_name if c not in dangerous_chars)
                # Remove leading/trailing spaces
                new_name = new_name.strip(" ")
                if not new_name:
                    new_name = f"{int(time.time())}{ext}"
                
                log.info(f"Auto-renamed: {filename} -> {new_name}")
                return new_name
            except KeyError as e:
                log.warning(f"Invalid variable in pattern: {e}, using original filename")
                return filename
        
        else:
            return filename
            
    except Exception as e:
        log.warning(f"Auto-rename failed: {e}, using original filename")
        return filename

__all__ = ["auto_rename_file"]
