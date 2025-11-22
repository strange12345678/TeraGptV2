import os
import time
import traceback
from typing import Dict, Any, Optional
from pyrogram import Client
from pyrogram.types import Message
from config import logger, Config
from .api import fetch_play_html, extract_direct_url_from_html, extract_filename
from .download import download_file
from .processing import generate_thumbnail, get_metadata, human_size
from .uploader import send_with_fallback
from plugins.error_channel import log_error
from plugins.log_channel import log_action
from plugins.storage_channel import backup_file

async def process_video(client: Client, message: Message, user_url: str) -> Dict[str, Any]:
    result = {"success": False, "file_path": None, "file_name": None, "metadata": None, "thumb": None, "error": None}
    file_path = None
    thumb = None
    fname = None
    status_msg = None
    try:
        # 1) basic validate
        if not user_url or not user_url.startswith("http"):
            raise ValueError("Invalid URL")

        # 2) create status message (used for progress)
        status_msg = await message.reply(Script := "⏳ Starting...")
        await status_msg.edit(Script := "🔎 " + "Extracting direct link...")

        # 3) fetch play page & extract direct url
        html = fetch_play_html(user_url)
        direct = extract_direct_url_from_html(html)
        if not direct:
            raise RuntimeError("Direct URL extraction failed")

        # 4) filename
        fname = extract_filename(html, direct)
        result["file_name"] = fname

        # 5) prepare local path
        os.makedirs(Config.DOWNLOAD_DIR, exist_ok=True)
        file_path = os.path.join(Config.DOWNLOAD_DIR, fname)
        result["file_path"] = file_path

        # 6) download with progress (edits status_msg)
        await status_msg.edit("📥 Downloading...")
        def dl_progress(curr, total):
            try:
                percent = (curr/total)*100 if total else 0.0
                bar = "▓" * int(percent/10) + "░" * (10 - int(percent/10))
                txt = f"📥 Downloading: {percent:.1f}%\n[{bar}]"
                client.loop.create_task(status_msg.edit(txt))
            except Exception:
                pass

        download_file(direct, file_path, progress=dl_progress, max_retries=2)
        logger.info(f"Downloaded file -> {file_path}")

        # 7) processing
        await status_msg.edit("📤 Preparing thumbnail & metadata...")
        thumb = generate_thumbnail(file_path)
        w,h,dur = get_metadata(file_path)
        result["metadata"] = {"width": w, "height": h, "duration": dur}
        result["thumb"] = thumb

        # 8) uploading
        await status_msg.edit("📤 Uploading to Telegram...")
        caption = f"✅ {fname}"
        sent = await send_with_fallback(client, message.chat.id, file_path, thumb, caption, width=w, height=h, duration=dur, progress_message=status_msg)

        # 9) backup to storage channel (non-blocking)
        try:
            size_text = human_size(file_path)
            await backup_file(client, file_path, fname, size_text, message.from_user.first_name or str(message.from_user.id), user_url)
        except Exception as e:
            logger.warning(f"Storage backup failed: {e}")
            await log_error(client, f"Storage backup failed: {e}")

        # 10) log action to log channel and console
        try:
            await log_action(client, message.from_user.id, f"Downloaded {fname}")
        except Exception as e:
            logger.warning(f"log_action failed: {e}")

        # 11) db log if you add later (skipped now)

        await status_msg.edit("✅ Completed.")
        result["success"] = True
        return result

    except Exception as exc:
        tb = traceback.format_exc()
        err = f"{type(exc).__name__}: {str(exc)}"
        result["error"] = err
        logger.error(f"Processing error: {err}\n{tb}")
        try:
            await log_error(client, err + "\n" + tb[:2000])
        except Exception:
            logger.exception("Failed to send error to ERROR_CHANNEL")
        try:
            if status_msg:
                await status_msg.edit("❌ Failed. See logs.")
        except:
            pass
        return result

    finally:
        # cleanup local files always
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass
        try:
            if thumb and os.path.exists(thumb):
                os.remove(thumb)
        except Exception:
            pass
