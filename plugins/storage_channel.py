import logging
from config import Config
from pyrogram import enums
from Theinertbotz.thumbnail import generate_thumbnail

log = logging.getLogger("TeraBoxBot")

async def backup_file(client, path: str, file_name: str, file_size: str, user: str, link: str) -> None:
    log.info(f"STORAGE: backup request {file_name} {file_size}")
    channel = Config.STORAGE_CHANNEL
    if not channel or channel == 0:
        log.debug(f"STORAGE_CHANNEL not configured, skipping backup")
        return
    try:
        user_str = f"@{user}" if user and user != "Unknown" else "Unknown"
        caption = f"<b>📂 File:</b> <code>{file_name}</code>\n<b>📊 Size:</b> {file_size}\n<b>👤 User:</b> {user_str}\n<b>🔗 Link:</b> <code>{link}</code>"
        
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
        thumbnail = None
        if is_video and size_bytes > 10 * 1024 * 1024:
            thumbnail = generate_thumbnail(path)
        
        # Send as video if it's a video file, otherwise as document
        if is_video:
            await client.send_video(
                chat_id=channel,
                video=path,
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                thumb=thumbnail
            )
        else:
            await client.send_document(
                chat_id=channel,
                document=path,
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
