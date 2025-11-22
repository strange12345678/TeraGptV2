# Theinertbotz/download.py
import aiohttp
import asyncio
import os
import time
from config import Config
from Theinertbotz.progress import ProgressManager
import logging

log = logging.getLogger("TeraBoxBot")
os.makedirs(Config.DOWNLOAD_DIR, exist_ok=True)

async def download_file(client, message, url: str, bot_username: str, kind="download"):
    """
    Streams the given download URL to disk and updates message progress using ProgressManager.
    Returns filepath on success.
    """
    # Create a status message
    status_msg = await message.reply("⏳ Fetching download...", parse_mode="html")

    async def edit_coro(text, parse_mode="html"):
        return await status_msg.edit_text(text, parse_mode=parse_mode)

    pm = ProgressManager(edit_coro, bot_username=bot_username, kind="download")

    filename = url.split("filename=")[-1] if "filename=" in url else f"{int(time.time())}.bin"
    safe_fn = "".join(c for c in filename if c.isalnum() or c in " .-_()[]{}%").strip()
    if not safe_fn:
        safe_fn = f"{int(time.time())}.bin"
    filepath = os.path.join(Config.DOWNLOAD_DIR, safe_fn)

    # stream via aiohttp
    CHUNK = 64 * 1024
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=120) as resp:
            resp.raise_for_status()
            total = int(resp.headers.get("Content-Length") or 0)
            processed = 0
            start = time.time()
            last_t = start
            last_bytes = 0

            with open(filepath, "wb") as f:
                async for chunk in resp.content.iter_chunked(CHUNK):
                    if not chunk:
                        continue
                    f.write(chunk)
                    processed += len(chunk)

                    # compute speed
                    now = time.time()
                    elapsed = now - last_t
                    if elapsed >= 0.5:
                        speed = (processed - last_bytes) / (now - last_t) if (now - last_t) else None
                        await pm.update(processed, total, speed)
                        last_t = now
                        last_bytes = processed

            # final update
            total_time = time.time() - start
            avg_speed = processed / total_time if total_time > 0 else 0
            await pm.update(processed, total, avg_speed)

    # final message update to indicate finished
    await status_msg.edit_text(f"<b>✅ Download complete:</b>\n{safe_fn}", parse_mode="html")
    log.info(f"Downloaded file -> {filepath}")
    return filepath, safe_fn
