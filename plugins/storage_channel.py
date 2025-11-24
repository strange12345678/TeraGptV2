import logging
import os
import shutil
import tempfile
from config import Config
from pyrogram import enums
from Theinertbotz.thumbnail import generate_thumbnail
from Theinertbotz.database import db
from Theinertbotz.rename import auto_rename_file

log = logging.getLogger("TeraBoxBot")

async def backup_file(client, path: str, file_name: str, file_size: str, user: str, link: str) -> None:
    log.info(f"STORAGE: backup request {file_name} {file_size}")
    channel = Config.STORAGE_CHANNEL
    if not channel or channel == 0:
        log.debug(f"STORAGE_CHANNEL not configured, skipping backup")
        return
    
    # Track files to clean up
    temp_file = None
    thumbnail = None
    upload_path = path  # Default: use original file
    display_name = file_name
    
    try:
        # Apply storage channel rename if enabled
        enabled, pattern = db.get_store_rename_setting()
        if enabled and pattern:
            # Parse file size for variables
            size_value = file_size.split()[0] if file_size else "unknown"
            variables = {
                "file_size": size_value,
                "user_id": user.replace("@", ""),  # Remove @ if present
                "username": user.replace("@", "")
            }
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
        
        # Check if it's a video file
        video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm')
        is_video = file_name.lower().endswith(video_extensions)
        
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
            await client.send_video(
                chat_id=channel,
                video=upload_path,
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                thumb=thumbnail
            )
        else:
            await client.send_document(
                chat_id=channel,
                document=upload_path,
                caption=caption,
                parse_mode=enums.ParseMode.HTML
            )
        
        log.debug(f"Backup sent to channel {channel}")
    except Exception as e:
        error_str = str(e)
        if "Peer id invalid" in error_str:
            log.error(f"Failed to backup to STORAGE_CHANNEL {channel}: Bot is not in the channel or channel ID is invalid. Add bot as admin and try again.")
        elif "USER_RESTRICTED" in error_str or "CHAT_SEND_PLAIN_FORBIDDEN" in error_str:
            log.error(f"Failed to backup to STORAGE_CHANNEL {channel}: Bot doesn't have permission to send messages. Check admin rights.")
        else:
            log.error(f"Failed to backup to STORAGE_CHANNEL {channel}: {e}")
    
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
