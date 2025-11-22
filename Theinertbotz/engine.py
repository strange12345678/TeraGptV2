import os
import time
import traceback
import asyncio
from typing import Dict, Any, Optional
from config import Config, logger
from .api import fetch_play_html, extract_direct_url_from_html, extract_filename
from .download import download_file
from .processing import generate_thumbnail, get_metadata, human_size
from .uploader import send_with_fallback
from .database import db
from plugins.error_channel import log_error
from plugins.log_channel import log_action
from plugins.storage_channel import backup_file

async def process_video(client, message, user_url: str) -> Dict[str, Any]:
    result = {"success": False, "file_path": None, "file_name": None, "metadata": None, "thumb": None, "error": None}
    file_path = None
    thumb = None
    fname = None
    status_msg = None
    try:
        if not user_url or not user_url.startswith("http"):
            raise ValueError("Invalid URL")
        status_msg = await message.reply("⏳ " + "Starting...")
        await status_msg.edit("🔎 " + "Extracting direct link...")

        # fetch HTML in thread
        loop = asyncio.get_running_loop()
        html = await loop.run_in_executor(None, fetch_play_html, user_url)
        direct = extract_direct_url_from_html(html)
        if not direct:
            raise RuntimeError("Direct URL extraction failed")

        fname = extract_filename(html, direct)
        result["file_name"] = fname

        os.makedirs(Config.DOWNLOAD_DIR, exist_ok=True)
        file_path = os.path.join(Config.DOWNLOAD_DIR, fname)
        result["file_path"] = file_path

        # prepare thread-safe progress callback
        def dl_progress(curr, total):
            try:
                percent = (curr/total)*100 if total else 0.0
                bar = "▓" * int(percent/10) + "░" * (10 - int(percent/10))
                txt = f"📥 Downloading: {percent:.1f}%\n[{bar}]"
                loop.call_soon_threadsafe(asyncio.create_task, status_msg.edit(txt))
            except Exception:
                pass

        await status_msg.edit("📥 Downloading...")
        # perform blocking download in thread
        await loop.run_in_executor(None, download_file, direct, file_path, dl_progress, 2)
        logger.info(f"Downloaded file -> {file_path}")

        await status_msg.edit("📤 Preparing thumbnail & metadata...")
        thumb = generate_thumbnail(file_path)
        w,h,dur = get_metadata(file_path)
        result["metadata"] = {"width": w, "height": h, "duration": dur}
        result["thumb"] = thumb

        await status_msg.edit("📤 Uploading to Telegram...")
        caption = f"✅ {fname}"
        await send_with_fallback(client, message.chat.id, file_path, thumb, caption, width=w, height=h, duration=dur, status_msg=status_msg)

        # backup (non-blocking)
        try:
            size_text = human_size(file_path)
            await backup_file(client, file_path, fname, size_text, message.from_user.first_name or str(message.from_user.id), user_url)
        except Exception as e:
            logger.warning(f"Storage backup failed: {e}")
            await log_error(client, f"Storage backup failed: {e}")

        # log & db
        try:
            await log_action(client, message.from_user.id, f"Downloaded {fname}")
        except Exception:
            pass
        db.add_user(message.from_user.id, message.from_user.first_name)
        db.log_download(message.from_user.id, fname, human_size(file_path))

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
            db.log_error(getattr(message.from_user, "id", 0), err)
        except Exception:
            logger.exception("Failed sending error to error channel or DB")
        try:
            if status_msg:
                await status_msg.edit("❌ Failed. See logs.")
        except:
            pass
        return result

    finally:
        # cleanup
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
