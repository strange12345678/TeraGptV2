
import os
import logging
from datetime import datetime

log = logging.getLogger("TeraBoxBot")

DEBUG_DIR = "debug_logs"

def save_html_debug(html: str, source: str = "unknown"):
    """Save HTML response for debugging purposes."""
    try:
        os.makedirs(DEBUG_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{DEBUG_DIR}/{source}_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        log.info(f"Saved HTML debug file: {filename}")
        return filename
    except Exception as e:
        log.error(f"Failed to save HTML debug file: {e}")
        return None

def extract_error_message(html: str):
    """Try to extract error message from HTML response."""
    import re
    
    error_patterns = [
        r'<div[^>]*class=["\']?error["\']?[^>]*>([^<]+)</div>',
        r'<p[^>]*class=["\']?error["\']?[^>]*>([^<]+)</p>',
        r'<span[^>]*class=["\']?error["\']?[^>]*>([^<]+)</span>',
        r'error["\']?\s*:\s*["\']([^"\']+)["\']',
        r'message["\']?\s*:\s*["\']([^"\']+)["\']',
    ]
    
    for pattern in error_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None
