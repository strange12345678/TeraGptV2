import os
import time
import logging
import asyncio
from pyrogram import enums
from Theinertbotz.processing import ProgressManager, human_size  # keep if used elsewhere

log = logging.getLogger("TeraBoxBot")


async def upload_file(client, message, filepath, bot_username: str):
    """
    Upload a file and update a status message with ProgressManager.
    Uses asyncio.run_coroutine_threadsafe(...) for safe scheduling from Pyrogram's worker thread.
    """

    # Create status message
    try:
        status_msg = await message.reply("⏳ Preparing upload...", quote=True, parse_mode=enums.ParseMode.HTML)
    except Exception:
        status_msg = await client.send_message(message.chat.id, "⏳ Preparing upload...")

    async def edit_coro(text, parse_mode=enums.ParseMode.HTML):
        return await status_msg.edit_text(text, parse_mode=parse_mode)

    # Initialize ProgressManager for upload
    pm = ProgressManager(edit_coro, bot_username=bot_username, kind="upload")

    total_size = os.path.getsize(filepath)
    state = {"last_time": time.time(), "last_bytes": 0}

    # capture the running loop to allow safe scheduling from other threads
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Fallback: create a new loop reference (shouldn't normally happen when called from async)
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

            # Schedule the coroutine safely on the captured loop
            try:
                asyncio.run_coroutine_threadsafe(coro, loop)
            except Exception as e:
                # If scheduling fails, log and continue — we do not want to crash the upload
                log.error(f"Failed to schedule progress update: {e}")

        except Exception as e:
            log.error(f"Upload progress callback failed: {e}")

    filename = os.path.basename(filepath)

    ############################################################################
    # Upload as video (Pyrogram handles chunking). Provide a simple caption.
    ############################################################################
    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=filepath,
            caption=f"<b>Uploaded:</b> {filename}",
            parse_mode=enums.ParseMode.HTML,
            supports_streaming=True,
            progress=_progress_cb,
            progress_args=()
        )

    except Exception as e:
        log.exception("upload failed")
        try:
            await status_msg.edit_text(f"❌ Upload failed:\n{str(e)}", parse_mode=enums.ParseMode.HTML)
        except Exception:
            pass
        raise

    # Final update (best-effort)
    try:
        await status_msg.edit_text(f"<b>✅ Upload complete:</b>\n{filename}", parse_mode=enums.ParseMode.HTML)
    except Exception:
        pass

    log.info(f"Uploaded file -> {filepath}")
