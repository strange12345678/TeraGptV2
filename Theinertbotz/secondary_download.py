# Theinertbotz/secondary_download.py
import subprocess
import os
import asyncio
import time
import logging
from pyrogram import enums
from config import Config
from Theinertbotz.processing import ProgressManager

log = logging.getLogger("TeraBoxBot")

os.makedirs(getattr(Config, "DOWNLOAD_DIR", "downloads"), exist_ok=True)


async def download_hls_video(client, message, m3u8_url: str, bot_username: str, filename: str = None):
    """
    Download HLS video (m3u8) using ffmpeg.
    Returns (filepath, safe_filename) on success.
    
    Args:
        client: pyrogram client
        message: incoming pyrogram Message
        m3u8_url: Direct m3u8 playlist URL
        bot_username: Bot username for display
        filename: Optional filename override
    """
    try:
        status_msg = await message.reply("⏳ sᴛᴀʀᴛɪɴɢ ʜʟs ᴅᴏᴡɴʟᴏᴀᴅ...", quote=True)
        await asyncio.sleep(2)
    except Exception:
        try:
            status_msg = await client.send_message(message.chat.id, "⏳ sᴛᴀʀᴛɪɴɢ ʜʟs ᴅᴏᴡɴʟᴏᴀᴅ...")
            await asyncio.sleep(2)
        except Exception:
            status_msg = None

    async def edit_coro(text, parse_mode=enums.ParseMode.HTML):
        if status_msg:
            try:
                await status_msg.edit_text(text, parse_mode=parse_mode)
            except Exception:
                pass

    pm = ProgressManager(edit_coro, bot_username=bot_username, kind="download")

    # Generate filename if not provided
    if not filename:
        timestamp = int(time.time())
        filename = f"video_{timestamp}.mp4"
    
    # Sanitize filename
    safe_fn = "".join(c for c in filename if c.isalnum() or c in " .-_()[]{}%").strip()
    if not safe_fn or safe_fn.lower().endswith(('.m3u8',)):
        safe_fn = f"video_{int(time.time())}.mp4"
    
    # Ensure .mp4 extension
    if not safe_fn.lower().endswith('.mp4'):
        safe_fn += ".mp4"
    
    filepath = os.path.join(getattr(Config, "DOWNLOAD_DIR", "downloads"), safe_fn)

    try:
        await edit_coro("⏳ <b>ꜰᴇᴛᴄʜɪɴɢ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ...</b>")
        
        # Build ffmpeg command
        # -c copy = stream copy without re-encoding (fastest)
        # -bsf:a aac_adtstoasc = convert AAC if needed
        cmd = [
            "ffmpeg",
            "-i", m3u8_url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-y",  # Overwrite output file
            filepath
        ]
        
        log.info(f"Running ffmpeg command for m3u8: {' '.join(cmd)}")
        
        # Run ffmpeg in executor
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        )
        
        if result.returncode != 0:
            error_out = result.stderr.decode() if result.stderr else "Unknown error"
            log.error(f"ffmpeg failed: {error_out}")
            await edit_coro(f"❌ <b>ꜰꜰᴍᴘᴇɢ ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ</b>\n\n{error_out[:200]}")
            return None, None
        
        if not os.path.exists(filepath):
            await edit_coro("❌ <b>ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ - ɴᴏ ꜰɪʟᴇ ᴄʀᴇᴀᴛᴇᴅ</b>")
            return None, None
        
        file_size = os.path.getsize(filepath)
        await edit_coro(f"✅ <b>ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ!</b>\n<code>{safe_fn}</code>\n🗂️ {file_size / (1024**2):.2f} MB")
        
        log.info(f"HLS download complete: {filepath} ({file_size} bytes)")
        return filepath, safe_fn

    except asyncio.CancelledError:
        log.warning(f"Download cancelled: {filepath}")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        await edit_coro("❌ <b>ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ</b>")
        return None, None

    except Exception as e:
        log.error(f"HLS download error: {e}", exc_info=True)
        await edit_coro(f"❌ <b>ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ:</b>\n<code>{str(e)[:100]}</code>")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        return None, None
