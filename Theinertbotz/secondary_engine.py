# Theinertbotz/secondary_engine.py
import asyncio
import logging
import os
from pyrogram import enums
from Theinertbotz.secondary_api import fetch_iteraplay_html, extract_m3u8_from_html, extract_video_info_from_html, extract_filename_from_terabox_html
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


async def process_video_secondary(client, message, user_url: str, status_msg=None) -> None:
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
        
        # Try to extract real filename from TeraBox HTML first
        loop = asyncio.get_running_loop()
        m3u8_url = None
        video_title = None
        
        # Extract actual filename from TeraBox page
        try:
            real_filename = await loop.run_in_executor(None, extract_filename_from_terabox_html, user_url)
            if real_filename:
                video_title = real_filename
                log.info(f"[SECONDARY API] Got filename from TeraBox HTML: {video_title}")
        except Exception as e:
            log.debug(f"[SECONDARY API] TeraBox filename extraction failed: {e}")
        
        # Try Playwright method first (most reliable - handles cookies and JS)
        try:
            from Theinertbotz.secondary_api_improved import extract_m3u8_with_playwright
            log.info(f"[SECONDARY API] Trying Playwright extraction...")
            m3u8_url, video_title_from_api = await extract_m3u8_with_playwright(user_url)
            if m3u8_url:
                log.info(f"[SECONDARY API] Got m3u8 from Playwright: {m3u8_url[:100]}...")
                # Use API title only if we didn't get one from TeraBox
                if not video_title and video_title_from_api:
                    video_title = video_title_from_api
        except Exception as pw_error:
            log.warning(f"[SECONDARY API] Playwright extraction failed: {pw_error}, trying fallback methods")
        
        # Fallback to direct API call if Playwright failed
        if not m3u8_url:
            try:
                from Theinertbotz.secondary_api import fetch_video_from_terabox_api
                log.info(f"[SECONDARY API] Trying direct API call...")
                m3u8_url, video_title = await loop.run_in_executor(
                    None, fetch_video_from_terabox_api, user_url
                )
                if m3u8_url:
                    log.info(f"[SECONDARY API] Got m3u8 from direct API: {m3u8_url[:100]}...")
            except Exception as api_error:
                log.warning(f"[SECONDARY API] Direct API failed: {api_error}, falling back to HTML extraction")
        
        # Fallback to HTML extraction if both methods failed
        if not m3u8_url:
            html = await loop.run_in_executor(None, fetch_iteraplay_html, user_url)
            log.info(f"[SECONDARY API] Fetched iTeraPlay HTML (len={len(html) if html else 0})")
            
            # Extract m3u8 URL
            m3u8_url = extract_m3u8_from_html(html)
            
            # Extract video info if not already set
            if not video_title:
                video_title = extract_video_info_from_html(html)

        if not m3u8_url:
            error_msg = f"[SECONDARY API] Failed to extract m3u8 URL from {user_url}"
            log.error(error_msg)
            await message.reply("❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴠɪᴅᴇᴏ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.", quote=True)
            await log_error(client, error_msg)
            return

        log.info(f"[SECONDARY API] Found m3u8: {m3u8_url}")
        log.info(f"[SECONDARY API] Video metadata - title: {video_title}")

        # Get bot username
        me = await client.get_me()
        bot_username = "@" + me.username if getattr(me, "username", None) else (me.first_name or "@bot")

        # Download HLS video (pass existing status_msg to update instead of creating new one)
        filepath, filename = await download_hls_video(client, message, m3u8_url, bot_username, video_title, status_msg=status_msg)
        
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

        # Upload to user - pass video_title as original filename for correct video detection
        await upload_file_secondary(client, message, filepath, bot_username, original_filename=video_title or filename)
        
        # Log download
        if uid:
            db.increment_daily_downloads(uid)
            await log_action(client, uid, f"✅ <b>ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ</b> ({file_size})\n<b>ᴜsᴇʀ:</b> @{username} (<code>{uid}</code>)\n<b>ʀᴀɴᴀᴍᴇ:</b> {filename}\n<b>ᴀᴘɪ:</b> sᴇᴄᴏɴᴅᴀʀʏ (ɪᴛᴇʀᴀᴘʟᴀʏ)")

        # Backup to storage channel - pass video_title as original filename for video detection
        if filename and uid:
            await backup_file(client, filepath, filename, file_size, f"@{username}", user_url, uid, video_title or filename)

        # Auto-upload to premium channel if applicable
        if filename and uid and db.is_premium_valid(uid):
            await upload_to_premium_channel(client, filepath, filename, file_size, uid, username)

        # Auto-delete if enabled (immediate deletion, no wait)
        if db.is_auto_delete_enabled() and filepath and os.path.exists(filepath):
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
