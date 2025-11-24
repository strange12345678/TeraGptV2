# Theinertbotz/secondary_upload.py
import os
import time
import logging
import asyncio
import subprocess
from pyrogram import enums
from Theinertbotz.processing import ProgressManager
from Theinertbotz.thumbnail import generate_thumbnail

log = logging.getLogger("TeraBoxBot")


def get_video_duration(filepath: str) -> int:
    """
    Extract video duration in seconds using ffprobe.
    Returns duration in seconds, or 0 if extraction fails.
    """
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filepath
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            duration = int(float(result.stdout.strip()))
            return duration
    except Exception as e:
        log.warning(f"Failed to extract video duration: {e}")
    return 0


async def upload_file_secondary(client, message, filepath, bot_username: str):
    """
    Upload a file for secondary API and update status message with ProgressManager.
    Handles both video and document uploads with thumbnail support.
    """

    # Create status message
    try:
        status_msg = await message.reply("⏳ ᴘʀᴇᴘᴀʀɪɴɢ ᴜᴘʟᴏᴀᴅ...", quote=True, parse_mode=enums.ParseMode.HTML)
        await asyncio.sleep(2)
    except Exception:
        try:
            status_msg = await client.send_message(message.chat.id, "⏳ ᴘʀᴇᴘᴀʀɪɴɢ ᴜᴘʟᴏᴀᴅ...")
            await asyncio.sleep(2)
        except Exception:
            status_msg = None

    async def edit_coro(text, parse_mode=enums.ParseMode.HTML):
        if status_msg:
            return await status_msg.edit_text(text, parse_mode=parse_mode)

    # Initialize ProgressManager for upload
    pm = ProgressManager(edit_coro, bot_username=bot_username, kind="upload")

    total_size = os.path.getsize(filepath)
    state = {"last_time": time.time(), "last_bytes": 0}

    # Capture the running loop for progress callback
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    # Progress callback invoked by Pyrogram from a worker thread
    def _progress_cb(current, total):
        try:
            now = time.time()
            elapsed = now - state["last_time"]
            if elapsed <= 0:
                elapsed = 0.001

            speed = (current - state["last_bytes"]) / elapsed
            state["last_bytes"] = current
            state["last_time"] = now

            coro = pm.update(current, total, speed)

            try:
                asyncio.run_coroutine_threadsafe(coro, loop)
            except Exception as e:
                log.error(f"Failed to schedule progress update: {e}")

        except Exception as e:
            log.error(f"Upload progress callback failed: {e}")

    filename = os.path.basename(filepath)

    # Generate/attach thumbnail for video files
    thumbnail_path = None
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm')
    
    # Check if it's a video - check full filename for video extensions
    # even if they're not at the very end (handles renamed files like video.mp4_2.6MB)
    is_video = any(ext in filename.lower() for ext in video_extensions)
    
    if is_video:
        # Look for existing thumbnail first
        base_name = os.path.splitext(filepath)[0]
        potential_thumb = f"{base_name}_thumb.jpg"
        
        if os.path.exists(potential_thumb):
            thumbnail_path = potential_thumb
            log.info(f"Using existing thumbnail: {thumbnail_path}")
        else:
            # Generate thumbnail
            thumbnail_path = generate_thumbnail(filepath)
            if thumbnail_path:
                log.info(f"Generated thumbnail: {thumbnail_path}")

    try:
        if is_video:
            # Upload as video with duration and thumbnail
            duration = get_video_duration(filepath)
            
            await client.send_video(
                message.chat.id,
                filepath,
                caption=f"<b>Uploaded:</b> {filename}",
                duration=duration,
                thumb=thumbnail_path,
                parse_mode=enums.ParseMode.HTML,
                supports_streaming=True,
                progress=_progress_cb,
                progress_args=()
            )
            
            # Clean up thumbnail
            if thumbnail_path and os.path.exists(thumbnail_path):
                try:
                    os.remove(thumbnail_path)
                except:
                    pass
        else:
            # Upload as document
            await client.send_document(
                message.chat.id,
                filepath,
                caption=f"<b>Uploaded:</b> {filename}",
                parse_mode=enums.ParseMode.HTML,
                progress=_progress_cb,
                progress_args=()
            )
        
        # Update final status
        await edit_coro(f"✅ <b>ᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ!</b>\n<code>{filename}</code>")
        log.info(f"[SECONDARY API] Upload completed: {filepath}")

    except Exception as e:
        log.error(f"[SECONDARY API] Upload failed: {e}", exc_info=True)
        await edit_coro(f"❌ <b>ᴜᴘʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ</b>\n<code>{str(e)[:100]}</code>")
        
        # Clean up thumbnail on error
        if thumbnail_path and os.path.exists(thumbnail_path):
            try:
                os.remove(thumbnail_path)
            except:
                pass
        
        raise
