import logging
import os
from config import Config
from pyrogram import enums
from Theinertbotz.thumbnail import generate_thumbnail
from Theinertbotz.database import db

log = logging.getLogger("TeraBoxBot")

async def upload_to_premium_channel(client, filepath: str, filename: str, file_size: str, user_id: int, username: str) -> None:
    """Upload downloaded file to premium channel for premium users only."""
    
    # Check if user is premium AND NOT expired
    if not db.is_premium_valid(user_id):
        return
    
    # Get channel from database first, fall back to config
    channel = db.get_premium_upload_channel()
    if not channel:
        channel = Config.PREMIUM_UPLOAD_CHANNEL
    
    if not channel or channel == 0:
        log.debug("PREMIUM_UPLOAD_CHANNEL not configured, skipping")
        return
    
    try:
        # Resolve channel peer first (required for new sessions)
        try:
            chat = await client.get_chat(channel)
            log.debug(f"Premium channel resolved: {chat.title if hasattr(chat, 'title') else channel}")
        except Exception as resolve_err:
            log.error(f"Failed to resolve PREMIUM_UPLOAD_CHANNEL {channel}: {resolve_err}")
            log.error(f"Make sure bot is added as ADMIN to the channel")
            return
        
        user_str = f"@{username}" if username and username != "Unknown" else f"User {user_id}"
        caption = f"<b>📂 File:</b> <code>{filename}</code>\n<b>📊 Size:</b> {file_size}\n<b>👤 User:</b> {user_str}\n<b>⏰ Premium Upload:</b> Auto-forwarded"
        
        # Check if it's a video file
        video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm')
        is_video = filename.lower().endswith(video_extensions)
        
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
        
        # Generate thumbnail for videos
        thumbnail = None
        if is_video and size_bytes > 5 * 1024 * 1024:
            thumbnail = generate_thumbnail(filepath)
        
        # Send as video if video file, otherwise as document
        if is_video:
            await client.send_video(
                chat_id=channel,
                video=filepath,
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                thumb=thumbnail
            )
        else:
            await client.send_document(
                chat_id=channel,
                document=filepath,
                caption=caption,
                parse_mode=enums.ParseMode.HTML
            )
        
        log.info(f"Uploaded {filename} to premium channel for user {user_id}")
        
        # Clean up thumbnail if created
        if thumbnail and os.path.exists(thumbnail):
            try:
                os.remove(thumbnail)
            except:
                pass
                
    except Exception as e:
        error_str = str(e)
        if "Peer id invalid" in error_str:
            log.error(f"Failed to upload to PREMIUM_UPLOAD_CHANNEL: Bot is not in the channel or channel ID is invalid. Add bot as admin and try again.")
        elif "USER_RESTRICTED" in error_str or "CHAT_SEND_PLAIN_FORBIDDEN" in error_str:
            log.error(f"Failed to upload to PREMIUM_UPLOAD_CHANNEL: Bot doesn't have permission to send messages. Check admin rights.")
        else:
            log.error(f"Failed to upload to PREMIUM_UPLOAD_CHANNEL: {e}")
