import os
import time
from datetime import datetime
import logging

log = logging.getLogger("TeraBoxBot")

def auto_rename_file(filename: str, pattern: str = "timestamp") -> str:
    """
    Auto-rename a file based on the specified pattern.
    
    Args:
        filename: Original filename
        pattern: Rename pattern - "timestamp" (default) or "counter"
    
    Returns:
        New filename with pattern applied
    """
    try:
        name, ext = os.path.splitext(filename)
        
        if pattern == "timestamp":
            # Format: original_name_YYYYMMDD_HHMMSS.ext
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{name}_{timestamp}{ext}"
            log.info(f"Auto-renamed: {filename} -> {new_name}")
            return new_name
        
        elif pattern == "datetime":
            # Format: original_name_YYYY-MM-DD_HH-MM-SS.ext
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_name = f"{name}_{timestamp}{ext}"
            log.info(f"Auto-renamed: {filename} -> {new_name}")
            return new_name
        
        else:
            # Default: return original filename
            return filename
            
    except Exception as e:
        log.warning(f"Auto-rename failed: {e}, using original filename")
        return filename

__all__ = ["auto_rename_file"]
