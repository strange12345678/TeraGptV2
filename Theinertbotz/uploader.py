# Theinertbotz/uploader.py
import os
import time
import logging
import asyncio
from Theinertbotz.processing import ProgressManager, human_size

log = logging.getLogger("TeraBoxBot")


async def upload_file(client, message, filepath, bot_username: str):
    """
    Upload a file to the user using Pyrogram's send_video() with
    a fully integrated ProgressManager for upload progress.

    Args:
        client: pyrogram client
        message: incoming message
        filepath: local file path to upload
        bot_username: bot's @username for progress display
    """

    # Create status message
    try:
        status_msg = await message.reply("⏳ Preparing upload...", quote=True, parse_mode="HTML")
    except Exception:
        status_msg = await client.send_message(message.chat.id, "⏳ Preparing upload...")

    async def edit_coro(text, parse_mode="HTML"):
        return await status_msg.edit_text(text, parse_mode=parse_mode)

    # Initialize Progress Manager for UPLOAD
    pm = ProgressManager(edit_coro, bot_username=bot_username, kind="upload")

    total_size = os.path.getsize(filepath)
    state = {"last_time": time.time(), "last_bytes": 0}

    # Progress callback
    def _progress_cb(current, total):
        """
        Pyrogram calls this in a worker thread.
        We schedule ProgressManager.update() back on the event loop.
        """
        try:
            now = time.time()
            elapsed = now - state["last_time"]
            if elapsed <= 0:
                elapsed = 0.001

            speed = (current - state["last_bytes"]) / elapsed
            state["last_bytes"] = current
            state["last_time"] = now

            coro = pm.update(current, total, speed)

            # Schedule coroutine safely
            asyncio.get_running_loop().create_task(coro)

        except Exception as e:
            log.error(f"Upload progress callback failed: {e}")

    filename = os.path.basename(filepath)

    ############################################################################
    # UPLOAD as VIDEO (auto detects mime type & sends as video with thumbnail)
    ############################################################################

    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=filepath,
            caption=f"<b>Uploaded:</b> {filename}",
            parse_mode="HTML",
            supports_streaming=True,
            progress=_progress_cb,
            progress_args=()
        )

    except Exception as e:
        log.exception("upload failed")
        try:
            await status_msg.edit_text(f"❌ Upload failed:\n{str(e)}", parse_mode="HTML")
        except:
            pass
        raise e

    ##########################################################################
    # Final message (when progress finishes)
    ##########################################################################
    try:
        await status_msg.edit_text(
            f"<b>✅ Upload complete:</b>\n{filename}",
            parse_mode="HTML"
        )
    except Exception:
        pass

    log.info(f"Uploaded file -> {filepath}")
