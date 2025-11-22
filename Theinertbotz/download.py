# Theinertbotz/download.py

import aiohttp
import asyncio
import os
import time
import logging

from config import Config
from Theinertbotz.processing import format_download_progress

log = logging.getLogger("TeraBoxBot")

os.makedirs(Config.DOWNLOAD_DIR, exist_ok=True)


async def download_file(client, message, url: str):
    """
    Streams the given TeraBox direct URL into disk.
    Uses format_download_progress() for non-spam progress updates.
    Returns (filepath, filename).
    """

    status_msg = await message.reply("⏳ Starting download...", parse_mode="html")

    # Detect filename
    filename = url.split("filename=")[-1] if "filename=" in url else f"{int(time.time())}.mp4"
    safe_fn = "".join(c for c in filename if c.isalnum() or c in " .-_()[]{}%").strip()
    if not safe_fn:
        safe_fn = f"{int(time.time())}.bin"

    filepath = os.path.join(Config.DOWNLOAD_DIR, safe_fn)

    CHUNK = 64 * 1024
    last_percentage = None
    downloaded = 0
    last_time = time.time()
    last_bytes = 0
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=200) as resp:
            resp.raise_for_status()

            total = int(resp.headers.get("Content-Length") or 0)
            log.info(f"[DOWNLOAD] Started -> {safe_fn}, size={total} bytes")

            with open(filepath, "wb") as f:
                async for chunk in resp.content.iter_chunked(CHUNK):
                    if not chunk:
                        continue

                    f.write(chunk)
                    downloaded += len(chunk)

                    # Progress calculation
                    now = time.time()
                    elapsed = now - last_time

                    if elapsed >= 1:  # update every 1 second
                        speed = (downloaded - last_bytes) / elapsed if elapsed > 0 else 0
                        eta = (total - downloaded) / speed if speed > 0 else 0

                        progress_text, last_percentage = await format_download_progress(
                            client,
                            downloaded,
                            total,
                            speed,
                            eta,
                            last_percentage
                        )

                        if progress_text:
                            try:
                                await status_msg.edit(progress_text)
                            except Exception:
                                pass

                        last_time = now
                        last_bytes = downloaded

            # FINAL UPDATE
            end_time = time.time()
            total_seconds = end_time - start_time
            avg_speed = downloaded / total_seconds if total_seconds > 0 else 0

            progress_text, _ = await format_download_progress(
                client, downloaded, total, avg_speed, 0, last_percentage
            )

            if progress_text:
                await status_msg.edit(progress_text)

    await status_msg.edit(f"<b>✅ Download Completed</b>\n📄 {safe_fn}", parse_mode="html")

    log.info(f"[DOWNLOAD] Completed -> {filepath}")

    return filepath, safe_fn
