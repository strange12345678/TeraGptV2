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

def apply_auto_rename(file_path, pattern, user_id=None, username=None):
    """
    Apply rename pattern to file_path.
    Returns new file path.
    """
    from datetime import datetime
    import os

    if not pattern:
        return file_path

    base = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]
    original_name = os.path.splitext(os.path.basename(file_path))[0]
    file_name_with_ext = os.path.basename(file_path)
    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    size_mb = file_size / (1024 * 1024)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    time_str = now.strftime("%H-%M-%S")
    datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Handle different built-in patterns
    if pattern == "timestamp":
        new_name = f"{original_name}_{timestamp_str}{ext}"
    elif pattern == "datetime":
        new_name = f"{original_name}_{datetime_str}{ext}"
    else:
        # Custom pattern with variables
        new_name = pattern
        new_name = new_name.replace("{file_name}", file_name_with_ext)
        new_name = new_name.replace("{original_name}", original_name)
        new_name = new_name.replace("{ext}", ext)
        new_name = new_name.replace("{file_size}", f"{size_mb:.2f}MB")
        new_name = new_name.replace("{date}", date_str)
        new_name = new_name.replace("{timestamp}", timestamp_str)
        new_name = new_name.replace("{time}", time_str)
        new_name = new_name.replace("{datetime}", datetime_str)

        if user_id:
            new_name = new_name.replace("{user_id}", str(user_id))
        if username:
            new_name = new_name.replace("{username}", username)

        # If pattern doesn't have extension, add it
        if not new_name.endswith(ext):
            new_name += ext

    new_path = os.path.join(base, new_name)

    try:
        os.rename(file_path, new_path)
        return new_path
    except Exception as e:
        import logging
        log = logging.getLogger("TeraBoxBot")
        log.error(f"Rename failed: {e}")
        return file_path


def apply_storage_rename(file_path, pattern, user_id=None, username=None):
    """
    Apply storage channel rename pattern by creating a copy.
    Returns path to renamed copy or original if rename fails.
    """
    from datetime import datetime
    import os
    import shutil

    if not pattern:
        return file_path

    base = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]
    original_name = os.path.splitext(os.path.basename(file_path))[0]
    file_name_with_ext = os.path.basename(file_path)
    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    size_mb = file_size / (1024 * 1024)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    time_str = now.strftime("%H-%M-%S")
    datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Apply custom pattern with variables
    new_name = pattern
    new_name = new_name.replace("{file_name}", file_name_with_ext)
    new_name = new_name.replace("{original_name}", original_name)
    new_name = new_name.replace("{ext}", ext)
    new_name = new_name.replace("{file_size}", f"{size_mb:.2f}MB")
    new_name = new_name.replace("{date}", date_str)
    new_name = new_name.replace("{timestamp}", timestamp_str)
    new_name = new_name.replace("{time}", time_str)
    new_name = new_name.replace("{datetime}", datetime_str)

    if user_id:
        new_name = new_name.replace("{user_id}", str(user_id))
    if username:
        new_name = new_name.replace("{username}", username)

    # If pattern doesn't have extension, add it
    if not new_name.endswith(ext):
        new_name += ext

    new_path = os.path.join(base, new_name)

    try:
        # Create a copy with the new name
        shutil.copy2(file_path, new_path)
        return new_path
    except Exception as e:
        import logging
        log = logging.getLogger("TeraBoxBot")
        log.error(f"Storage rename failed: {e}")
        return file_path


__all__ = ["auto_rename_file", "apply_auto_rename", "apply_storage_rename"]