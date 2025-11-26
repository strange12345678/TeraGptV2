import logging
import os
import shutil
import tempfile
from typing import Optional
from config import Config
from pyrogram import enums
from Theinertbotz.thumbnail import generate_thumbnail
from Theinertbotz.database import db
from Theinertbotz.rename import auto_rename_file, apply_storage_rename

log = logging.getLogger("TeraBoxBot")

def validate_channel_id(channel_id) -> bool:
    """Validate if channel ID is in correct format for Telegram API"""
    if not channel_id:
        return False
    
    try:
        ch = int(channel_id)
        if ch == 0:
            return False
        if ch > 0:
            log.warning(f"Channel ID {ch} is positive - should be negative for channels/groups. Attempting to use as-is.")
        return True
    except (ValueError, TypeError):
        return False

async def backup_file(client, path: str, file_name: str, file_size: str, user: str, link: str, user_id: Optional[int] = None, original_filename: Optional[str] = None) -> None:
    log.info(f"STORAGE: backup request {file_name} {file_size}")
    log.info(f"[STORAGE] 🔍 PARAMETERS: file_name='{file_name}', original_filename='{original_filename}', user_id={user_id}")
    channel = Config.STORAGE_CHANNEL
    
    # Validate channel configuration
    if not channel:
        log.debug(f"STORAGE_CHANNEL not configured (None), skipping backup")
        return
    if channel == 0:
        log.debug(f"STORAGE_CHANNEL not configured (0), skipping backup")
        return
    
    # Validate channel ID format
    if not validate_channel_id(channel):
        log.error(f"STORAGE_CHANNEL {channel} is invalid format. Must be a negative integer like -1001234567890")
        return

    # Track files to clean up
    temp_file = None
    thumbnail = None
    upload_path = path  # Default: use original file
    display_name = file_name

    try:
        # Resolve channel peer first (required for new sessions)
        try:
            chat = await client.get_chat(channel)
            log.info(f"[STORAGE] Resolved channel: {chat.title if hasattr(chat, 'title') else channel}")
        except Exception as resolve_err:
            log.error(f"[STORAGE] Failed to resolve channel {channel}: {resolve_err}")
            log.error(f"[STORAGE] Make sure bot is added as ADMIN to the channel")
            return
        
        # Apply storage channel rename if enabled
        enabled, pattern = db.get_store_rename_setting()
        if enabled and pattern:
            # Parse file size for variables
            size_value = file_size.split()[0] if file_size else "unknown"
            # Clean username: remove @ prefix if present
            clean_username = user.replace("@", "") if user else "unknown"
            variables = {
                "file_size": size_value,
                "user_id": str(user_id) if user_id else "unknown",
                "username": clean_username
            }
            log.info(f"[STORAGE] Variables for rename: user_id={variables['user_id']}, username={variables['username']}, pattern={pattern}")
            renamed = auto_rename_file(file_name, pattern, variables)
            if renamed != file_name:
                display_name = renamed

                # Create a temporary copy with the new name
                temp_dir = tempfile.gettempdir()
                temp_file = os.path.join(temp_dir, display_name)
                shutil.copy2(path, temp_file)
                upload_path = temp_file

                log.info(f"[STORAGE] Renamed for channel: {file_name} -> {display_name}")
                log.info(f"[STORAGE] Using temp file: {upload_path}")

        user_str = f"@{user}" if user and user != "Unknown" else "Unknown"
        caption = f"<b>📂 File:</b> <code>{display_name}</code>\n<b>📊 Size:</b> {file_size}\n<b>👤 User:</b> {user_str}\n<b>🔗 Link:</b> <code>{link}</code>"

        # Check if it's a video file - use original filename for detection if available
        video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm')
        detection_name = original_filename or file_name
        # Check if the detection name contains a video extension
        is_video = any(ext in detection_name.lower() for ext in video_extensions)
        
        # Debug: Check each extension
        for ext in video_extensions:
            if ext in detection_name.lower():
                log.info(f"[STORAGE] ✅ Found extension '{ext}' in '{detection_name}'")
        
        log.info(f"[STORAGE] Video detection: original_filename={original_filename}, file_name={file_name}, detection_name={detection_name}, is_video={is_video}")
        if is_video:
            log.info(f"[STORAGE] ✅ WILL SEND AS VIDEO")
        else:
            log.info(f"[STORAGE] ❌ WILL SEND AS DOCUMENT")

        # Parse file size to get bytes
        size_bytes = 0
        try:
            if 'MB' in file_size:
                size_bytes = int(float(file_size.split()[0]) * 1024 * 1024)
            elif 'KB' in file_size:
                size_bytes = int(float(file_size.split()[0]) * 1024)
            elif 'GB' in file_size:
                size_bytes = int(float(file_size.split()[0]) * 1024 * 1024 * 1024)
        except:
            pass

        # Generate thumbnail for videos > 10MB
        if is_video and size_bytes > 10 * 1024 * 1024:
            thumbnail = generate_thumbnail(upload_path)

        # Send as video if it's a video file, otherwise as document
        if is_video:
            log.info(f"[STORAGE] 📤 SENDING VIDEO: upload_path={upload_path}, thumbnail={thumbnail}")
            try:
                await client.send_video(
                    chat_id=channel,
                    video=upload_path,
                    caption=caption,
                    parse_mode=enums.ParseMode.HTML,
                    thumb=thumbnail
                )
                log.info(f"[STORAGE] ✅ VIDEO SENT SUCCESSFULLY to channel {channel}")
            except Exception as e:
                log.error(f"[STORAGE] ❌ FAILED TO SEND VIDEO: {e}")
                raise
        else:
            log.info(f"[STORAGE] 📄 SENDING DOCUMENT: upload_path={upload_path}")
            await client.send_document(
                chat_id=channel,
                document=upload_path,
                caption=caption,
                parse_mode=enums.ParseMode.HTML
            )
            log.info(f"[STORAGE] ✅ DOCUMENT SENT to channel {channel}")
    except Exception as e:
        error_str = str(e)
        log.error(f"STORAGE_CHANNEL send error: {type(e).__name__}: {error_str}")
        
        if "Peer id invalid" in error_str or "chat not found" in error_str.lower():
            log.error(f"Failed to backup to STORAGE_CHANNEL {channel}: Bot is not an admin or channel doesn't exist. Ensure bot is added as ADMIN with full permissions.")
        elif "USER_RESTRICTED" in error_str or "CHAT_SEND_PLAIN_FORBIDDEN" in error_str:
            log.error(f"Failed to backup to STORAGE_CHANNEL {channel}: Bot doesn't have permission to post. Check bot admin rights.")
        elif "auth" in error_str.lower() or "unauthorized" in error_str.lower():
            log.error(f"Failed to backup to STORAGE_CHANNEL {channel}: Authentication issue - bot may not be properly authenticated.")
        else:
            log.error(f"Failed to backup to STORAGE_CHANNEL {channel}: {type(e).__name__} - {error_str}")

    finally:
        # Clean up temporary files
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                log.info(f"[STORAGE] Cleaned up temp file: {temp_file}")
            except Exception as e:
                log.warning(f"[STORAGE] Failed to clean temp file: {e}")

        if thumbnail and os.path.exists(thumbnail):
            try:
                os.remove(thumbnail)
            except:
                pass

async def send_to_storage(client, file_path, user_id, file_type="video"):
    """Upload file to storage channel with metadata and optional rename."""
    from config import Config
    from Theinertbotz.database import db
    from Theinertbotz.rename import apply_storage_rename
    import logging
    from pyrogram import enums
    import os
    import shutil

    log = logging.getLogger("TeraBoxBot")

    if not Config.STORAGE_CHANNEL:
        log.warning("STORAGE_CHANNEL not configured")
        return None

    try:
        # Resolve channel peer first (required for new sessions)
        try:
            chat = await client.get_chat(Config.STORAGE_CHANNEL)
            log.info(f"[STORAGE] Resolved channel: {chat.title if hasattr(chat, 'title') else Config.STORAGE_CHANNEL}")
        except Exception as resolve_err:
            log.error(f"[STORAGE] Failed to resolve channel {Config.STORAGE_CHANNEL}: {resolve_err}")
            return None
        
        original_file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        size_mb = file_size / (1024 * 1024)

        # Check if storage rename is enabled and apply pattern
        enabled, pattern = db.get_store_rename_setting()

        upload_path = file_path
        final_file_name = original_file_name

        if enabled and pattern:
            # Apply rename pattern for storage channel
            try:
                # Get user info for variables
                user = await client.get_users(user_id)
                username = user.username if user.username else f"user{user_id}"

                # Apply storage rename
                renamed_file = apply_storage_rename(
                    file_path=file_path,
                    pattern=pattern,
                    user_id=user_id,
                    username=username
                )

                if renamed_file and renamed_file != file_path:
                    upload_path = renamed_file
                    final_file_name = os.path.basename(renamed_file)
                    log.info(f"Storage rename applied: {original_file_name} -> {final_file_name}")
            except Exception as e:
                log.error(f"Storage rename failed, using original name: {e}")

        caption = f"""
📦 <b>Storage Backup</b>

📄 <b>File:</b> <code>{final_file_name}</code>
👤 <b>User ID:</b> <code>{user_id}</code>
📊 <b>Size:</b> {size_mb:.2f} MB
"""

        if file_type == "video":
            msg = await client.send_video(
                chat_id=Config.STORAGE_CHANNEL,
                video=upload_path,
                caption=caption,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            msg = await client.send_document(
                chat_id=Config.STORAGE_CHANNEL,
                document=upload_path,
                caption=caption,
                parse_mode=enums.ParseMode.HTML
            )

        # Clean up renamed file if it was created
        if upload_path != file_path and os.path.exists(upload_path):
            try:
                os.remove(upload_path)
            except:
                pass

        log.info(f"File {final_file_name} backed up to storage channel")
        return msg

    except Exception as e:
        log.exception(f"Failed to send to storage: {e}")
        return None