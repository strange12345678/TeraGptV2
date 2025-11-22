# Theinertbotz/download.py
import aiohttp
import asyncio
import os
import time
import logging
from pyrogram import enums
from config import Config
from Theinertbotz.processing import ProgressManager
from Theinertbotz.rename import auto_rename_file
log = logging.getLogger("TeraBoxBot")

os.makedirs(getattr(Config, "DOWNLOAD_DIR", "downloads"), exist_ok=True)

async def download_file(client, message, url: str, bot_username: str, kind: str = "download"):
    """
    Streams the given download URL to disk and updates message progress using ProgressManager.
    Returns (filepath, safe_filename) on success.
    Args:
      client: pyrogram client (not used heavily here, kept for parity)
      message: incoming pyrogram Message (used for replies/edit)
      url: direct download URL
      bot_username: string like "@inert_test_bot" (for display)
      kind: "download" (default)
    """
    # Create a status message
    try:
        status_msg = await message.reply("⏳ Fetching download...", quote=True)
    except Exception:
        # fallback: send_message
        status_msg = await client.send_message(message.chat.id, "⏳ Fetching download...")

    async def edit_coro(text, parse_mode=enums.ParseMode.HTML):
        return await status_msg.edit_text(text, parse_mode=parse_mode)

    pm = ProgressManager(edit_coro, bot_username=bot_username, kind=kind)

    # derive filename
    filename = None
    # try common query param
    try:
        from urllib.parse import urlparse, parse_qs, unquote
        qp = parse_qs(urlparse(url).query)
        if "filename" in qp and qp["filename"]:
            filename = unquote(qp["filename"][0])
        elif "fin" in qp and qp["fin"]:
            filename = unquote(qp["fin"][0])
    except Exception:
        filename = None

    if not filename:
        # fallback to last path segment
        try:
            filename = os.path.basename(url.split("?")[0])
        except Exception:
            filename = None

    if not filename:
        filename = f"{int(time.time())}.bin"

    safe_fn = "".join(c for c in filename if c.isalnum() or c in " .-_()[]{}%").strip()
    if not safe_fn:
        safe_fn = f"{int(time.time())}.bin"
    
    # Apply auto-rename if enabled
    rename_pattern = getattr(Config, "AUTO_RENAME", "")
    if rename_pattern:
        safe_fn = auto_rename_file(safe_fn, rename_pattern)
    
    filepath = os.path.join(getattr(Config, "DOWNLOAD_DIR", "downloads"), safe_fn)

    CHUNK = 64 * 1024
    timeout = aiohttp.ClientTimeout(total=0, sock_read=120)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    max_retries = 2
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    total = int(resp.headers.get("Content-Length") or 0)
                    processed = 0
                    start = time.time()
                    last_t = start
                    last_bytes = 0

                    # write streaming
                    with open(filepath, "wb") as f:
                        async for chunk in resp.content.iter_chunked(CHUNK):
                            if not chunk:
                                continue
                            f.write(chunk)
                            processed += len(chunk)

                            # compute speed & update every ~0.5s (ProgressManager will throttle)
                            now = time.time()
                            elapsed = now - last_t
                            if elapsed >= 0.5:
                                speed = (processed - last_bytes) / elapsed if (elapsed > 0) else None
                                try:
                                    await pm.update(processed, total, speed)
                                except Exception:
                                    log.exception("pm.update failed during download")
                                last_t = now
                                last_bytes = processed

                    # final update
                    total_time = time.time() - start
                    avg_speed = processed / total_time if total_time > 0 else 0
                    try:
                        await pm.update(processed, total, avg_speed)
                    except Exception:
                        log.exception("pm.update final failed")

            # final message update to indicate finished
            try:
                await status_msg.edit_text(f"<b>✅ Download complete:</b>\n{safe_fn}", parse_mode=enums.ParseMode.HTML)
            except Exception:
                try:
                    await client.send_message(message.chat.id, f"✅ Download complete: {safe_fn}")
                except Exception:
                    pass

            log.info(f"Downloaded file -> {filepath}")
            return filepath, safe_fn
        except aiohttp.ClientPayloadError as e:
            if attempt < max_retries - 1:
                log.warning(f"Download attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(2)
                continue
            else:
                log.exception(f"Download failed after {max_retries} attempts")
                try:
                    await status_msg.edit_text(f"❌ Download failed: Server connection error\nPlease try again", parse_mode=enums.ParseMode.HTML)
                except Exception:
                    pass
                raise Exception("Server connection interrupted. Please try again.")
        except Exception as e:
            log.exception(f"Download failed for {url}")
            try:
                await status_msg.edit_text(f"❌ Processing Error: Failed to download file. Please try again.", parse_mode=enums.ParseMode.HTML)
            except Exception:
                pass
            raise
        break  # Success, exit retry loop