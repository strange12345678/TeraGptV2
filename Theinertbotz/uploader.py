# Theinertbotz/uploader.py
import os
import math
import time
import logging
from Theinertbotz.progress import ProgressManager, human_size
log = logging.getLogger("TeraBoxBot")

async def upload_file(client, message, filepath, bot_username):
    # Send a placeholder message
    status_msg = await message.reply("⏳ Preparing upload...", parse_mode="html")

    async def edit_coro(text, parse_mode="html"):
        return await status_msg.edit_text(text, parse_mode=parse_mode)

    pm = ProgressManager(edit_coro, bot_username=bot_username, kind="upload")

    total = os.path.getsize(filepath)
    start = time.time()
    state = {"last_bytes": 0, "last_time": start}

    # Pyrogram progress callback signature: (current, total)
    def _progress_cb(current, total_bytes):
        # schedule coroutine update safely
        now = time.time()
        elapsed = now - state["last_time"]
        if elapsed <= 0:
            elapsed = 0.0001
        speed = (current - state["last_bytes"]) / elapsed
        state["last_time"] = now
        state["last_bytes"] = current

        # create coroutine to update progress manager
        coro = pm.update(current, total_bytes, speed)
        # schedule on loop properly
        try:
            import asyncio
            asyncio.create_task(coro)
        except Exception:
            # If scheduling fails, ignore; the main flow will continue
            log.exception("Failed to schedule progress coroutine")

    # Send as video (Pyrogram will use its own media methods)
    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=filepath,
            caption=f"Uploaded: {os.path.basename(filepath)}",
            progress=_progress_cb,
            progress_args=()
        )
    except Exception as e:
        log.exception("upload failed")
        raise
    finally:
        try:
            await status_msg.edit_text(f"<b>✅ Upload complete:</b>\n{os.path.basename(filepath)}", parse_mode="html")
        except:
            pass

    log.info(f"Uploaded file {filepath}")
