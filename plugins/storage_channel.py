import logging
import os
import shutil
import tempfile
from config import Config
from pyrogram import enums
from Theinertbotz.thumbnail import generate_thumbnail
from Theinertbotz.database import db
from Theinertbotz.rename import auto_rename_file, apply_storage_rename

log = logging.getLogger("TeraBoxBot")

async def backup_file(client, path: str, file_name: str, file_size: str, user: str, link: str, user_id: int = None, original_filename: str = None) -> None:
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
        is_video_file = any(ext in detection_name.lower() for ext in video_extensions)
        
        # Only send as video format if user is admin
        from handlers.admin import is_admin
        is_video = is_video_file and is_admin(user_id) if user_id else False
        log.info(f"[STORAGE] Video detection: original={original_filename}, file_name={file_name}, user_id={user_id}, is_admin={is_admin(user_id) if user_id else False}, is_video={is_video}")

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