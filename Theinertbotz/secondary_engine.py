# Theinertbotz/secondary_engine.py
import asyncio
import logging
import os
from pyrogram import enums
from Theinertbotz.secondary_api import fetch_iteraplay_html, extract_m3u8_from_html, extract_m3u8_with_browser, extract_video_info_from_html
from Theinertbotz.secondary_download import download_hls_video
from Theinertbotz.secondary_upload import upload_file_secondary
from Theinertbotz.thumbnail import generate_thumbnail
from Theinertbotz.processing import human_size
from Theinertbotz.database import db
from plugins.log_channel import log_action
from plugins.error_channel import log_error
from plugins.storage_channel import backup_file
from plugins.premium_upload import upload_to_premium_channel

log = logging.getLogger("TeraBoxBot")


async def process_video_secondary(client, message, user_url: str) -> None:
    """
    Process video using iTeraPlay secondary API.
    Extracts m3u8 from HTML and downloads using ffmpeg.
    """
    from typing import Optional
    uid: Optional[int] = getattr(message.from_user, "id", None)
    username: str = getattr(message.from_user, "username", "Unknown") or "Unknown"
    filename: Optional[str] = None
    filepath: Optional[str] = None
    
    try:
        log.info(f"[SECONDARY API] Processing link: {user_url} from user {uid}")
        
        # Try to extract m3u8 using headless browser (handles JavaScript-loaded streams)
        log.info(f"[SECONDARY API] Attempting browser-based extraction...")
        m3u8_url = await extract_m3u8_with_browser(user_url)
        
        # Fallback: try static HTML extraction if browser failed
        if not m3u8_url:
            log.info(f"[SECONDARY API] Browser extraction failed, trying static HTML...")
            loop = asyncio.get_running_loop()
            html = await loop.run_in_executor(None, fetch_iteraplay_html, user_url)
            log.info(f"[SECONDARY API] Fetched iTeraPlay HTML (len={len(html) if html else 0})")
            m3u8_url = extract_m3u8_from_html(html)

        if not m3u8_url:
            error_msg = f"[SECONDARY API] Failed to extract m3u8 URL from {user_url}"
            await message.reply("❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ.", quote=True)
            await log_error(client, error_msg)
            return

        log.info(f"[SECONDARY API] Found m3u8: {m3u8_url}")

        # Extract video info for filename
        video_title = extract_video_info_from_html(html)

        # Get bot username
        me = await client.get_me()
        bot_username = "@" + me.username if getattr(me, "username", None) else (me.first_name or "@bot")

        # Download HLS video
        filepath, filename = await download_hls_video(client, message, m3u8_url, bot_username, video_title)
        
        if not filepath or not os.path.exists(filepath):
            error_msg = f"[SECONDARY API] HLS download failed for {user_url}"
            await log_error(client, error_msg)
            return

        # Get file size
        file_size = human_size(os.path.getsize(filepath)) if os.path.exists(filepath) else "Unknown"

        # Generate thumbnail
        thumb_path = None
        if filename and filename.lower().endswith(('.mp4', '.mkv', '.mov', '.webm')):
            thumb_path = generate_thumbnail(filepath)

        # Upload to user
        await upload_file_secondary(client, message, filepath, bot_username)
        
        # Log download
        if uid:
            db.increment_daily_downloads(uid)
            await log_action(client, f"✅ <b>ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ</b> ({file_size})\n<b>ᴜsᴇʀ:</b> @{username} (<code>{uid}</code>)\n<b>ʀᴀɴᴀᴍᴇ:</b> {filename}\n<b>ᴀᴘɪ:</b> sᴇᴄᴏɴᴅᴀʀʏ (ɪᴛᴇʀᴀᴘʟᴀʏ)")

        # Backup to storage channel
        await backup_file(client, filepath, filename, f"@{username}")

        # Auto-upload to premium channel if applicable
        if uid and db.is_premium_valid(uid):
            await upload_to_premium_channel(client, filepath, filename, uid, thumb_path)

        # Auto-delete if enabled
        auto_delete_time = db.get_auto_delete_time()
        if auto_delete_time and filepath and os.path.exists(filepath):
            await asyncio.sleep(auto_delete_time)
            try:
                os.remove(filepath)
                log.info(f"Auto-deleted: {filepath}")
            except Exception as e:
                log.warning(f"Auto-delete failed: {e}")

    except Exception as e:
        log.error(f"[SECONDARY API] Error processing video: {e}", exc_info=True)
        error_msg = f"[SECONDARY API] Exception: {str(e)[:100]}"
        await message.reply("❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴅᴜʀɪɴɢ ᴘʀᴏᴄᴇssɪɴɢ.", quote=True)
        await log_error(client, error_msg)
