# Theinertbotz/uploader.py

import os
import time
import asyncio
import logging

from Theinertbotz.processing import format_upload_progress

log = logging.getLogger("TeraBoxBot")


async def upload_file(client, message, filepath):
    """
    Upload file to Telegram with beautiful progress bar.
    """

    filename = os.path.basename(filepath)
    status_msg = await message.reply("⏳ Preparing upload...", parse_mode="html")

    total = os.path.getsize(filepath)
    last_percentage = None

    # Track speed
    last_time = time.time()
    last_bytes = 0

    # Progress callback (Pyrogram-style)
    async def update_progress(current, total_bytes):
        nonlocal last_bytes, last_time, last_percentage

        now = time.time()
        elapsed = now - last_time
        if elapsed <= 0:
            elapsed = 0.1

        speed = (current - last_bytes) / elapsed
        eta = (total_bytes - current) / speed if speed > 0 else 0

        # Format upload progress
        formatted, last_percentage = await format_upload_progress(
            client,
            current,
            total_bytes,
            speed,
            eta,
            last_percentage
        )

        if formatted:
            try:
                await status_msg.edit_text(formatted)
            except Exception:
                pass

        last_time = now
        last_bytes = current

    # Wrapper so Pyrogram can call async update
    def progress_cb(current, total_bytes):
        asyncio.create_task(update_progress(current, total_bytes))

    # Upload as VIDEO (not document)
    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=filepath,
            caption=f"<b>📤 Uploaded:</b> {filename}",
            parse_mode="html",
            supports_streaming=True,
            progress=progress_cb,
        )
    except Exception as e:
        log.exception("Upload failed")
        await status_msg.edit("<b>❌ Upload Failed!</b>", parse_mode="html")
        raise e

    # Final message
    try:
        await status_msg.edit(f"<b>✅ Upload Complete:</b>\n{filename}", parse_mode="html")
    except:
        pass

    log.info(f"[UPLOAD] Completed -> {filepath}")
