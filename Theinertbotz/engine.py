# Theinertbotz/engine.py
import asyncio
import logging
import time
from urllib.parse import unquote

from Theinertbotz.api import fetch_play_html
from Theinertbotz.download import download_file
from Theinertbotz.uploader import upload_file
from Theinertbotz.database import db
from config import Config

log = logging.getLogger("TeraBoxBot")

# Global semaphore to enforce one-at-a-time processing (Option A)
# If you prefer per-user queueing later, we can change this to a dict of semaphores keyed by user id.
GLOBAL_PROCESS_SEMAPHORE = asyncio.Semaphore(1)


async def process_video(client, message, user_url: str):
    """
    Main processing pipeline:
      1) Fetch play page HTML via fetch_play_html (it should call the /play API)
      2) Extract direct link with heuristics (find_direct_link_from_html found in engine import context)
      3) Download file (download_file)
      4) Upload file to user (upload_file)
      5) Backup to storage channel + log to log channel + DB entry
    This function acquires GLOBAL_PROCESS_SEMAPHORE so only one process runs at a time.
    """
    uid = None
    try:
        uid = message.from_user.id if message.from_user else None
        user_display = f"{message.from_user.first_name} ({uid})" if uid else "unknown"

        # Acquire the global semaphore (Option A: process links serially)
        log.info(f"Waiting for global lock to process link: {user_url} (from {user_display})")
        async with GLOBAL_PROCESS_SEMAPHORE:
            log.info(f"Processing link: {user_url} from user {uid}")

            # Fetch the play HTML via your API wrapper (synchronous requests run in executor)
            loop = asyncio.get_event_loop()
            start_fetch = time.time()
            try:
                html = await loop.run_in_executor(None, fetch_play_html, user_url)
            except Exception as e:
                log.exception("Failed fetching play HTML")
                await _notify_user_and_channels_on_error(client, message, user_url, f"Fetch error: {e}")
                return
            fetch_time = time.time() - start_fetch
            log.info(f"Fetched play HTML in {fetch_time:.2f}s (len={len(html) if html else 0})")

            # Try to extract direct link using heuristics defined elsewhere in this file's module scope.
            direct_link = await _find_direct_link(html)
            if not direct_link:
                log.warning("Direct link not found in play HTML")
                await _notify_user_and_channels_on_error(
                    client,
                    message,
                    user_url,
                    "❌ Failed to extract direct link from play HTML."
                )
                return

            log.info(f"Found direct link -> {direct_link}")

            # Get bot username for nicer progress (if your download expects it)
            try:
                me = await client.get_me()
                bot_username = ("@" + me.username) if getattr(me, "username", None) else me.first_name
            except Exception:
                bot_username = None

            # Download the file (download_file should return (filepath, filename))
            try:
                filepath, filename = await download_file(client, message, direct_link, bot_username)
            except Exception as e:
                log.exception("Download failed")
                await _notify_user_and_channels_on_error(client, message, user_url, f"Download error: {e}")
                return

            # Upload to user (uploader signature you used previously accepts bot_username)
            try:
                # If your uploader signature doesn't accept bot_username, remove it accordingly.
                try:
                    await upload_file(client, message, filepath, bot_username)
                except TypeError:
                    # fallback if uploader uses the other signature (client, message, filepath)
                    await upload_file(client, message, filepath)
            except Exception as e:
                log.exception("Upload failed")
                # still attempt to notify channels and keep file for debugging
                await _notify_user_and_channels_on_error(client, message, user_url, f"Upload error: {e}")
                return

            # DB logging
            try:
                if uid:
                    db.add_log(uid, filename)
            except Exception:
                log.exception("DB logging failed")

            # Backup to STORAGE_CHANNEL (best-effort)
            try:
                if hasattr(Config, "STORAGE_CHANNEL") and Config.STORAGE_CHANNEL:
                    # send_document is a safer backup; use caption with user info
                    caption = f"📂 Stored by: <code>{uid}</code>\nFile: {filename}"
                    await client.send_document(Config.STORAGE_CHANNEL, document=filepath, caption=caption, parse_mode="html")
            except Exception as e:
                log.warning("Failed to backup to STORAGE_CHANNEL: %s", e)

            # Admin log
            try:
                if hasattr(Config, "LOG_CHANNEL") and Config.LOG_CHANNEL:
                    await client.send_message(Config.LOG_CHANNEL, f"LOG: user={uid} downloaded {filename}")
            except Exception as e:
                log.warning("Failed to send to LOG_CHANNEL: %s", e)

            # Final user confirmation (single message)
            try:
                await message.reply(f"✅ Done: <b>{filename}</b>", parse_mode="html", quote=True)
            except Exception:
                pass

    except Exception as e:
        log.exception("Unhandled processing error")
        try:
            await _notify_user_and_channels_on_error(client, message, user_url, f"Unhandled error: {e}")
        except Exception:
            log.exception("Also failed to notify user")
    finally:
        log.info(f"Finished processing: {user_url} for user {uid}")


# -------------------------
# Helper utilities
# -------------------------
async def _find_direct_link(html: str):
    """
    Wrapper to call the heuristic extractor available at module scope:
    - prefer exact JS assignment matches, then candidate patterns, then generic urls.
    If `find_direct_link_from_html` exists in module (older versions), call it.
    """
    # Many of your earlier heuristics were top-level async functions; try to call them if present.
    try:
        # If the helper exists in module namespace (older code had find_direct_link_from_html)
        finder = globals().get("find_direct_link_from_html")
        if finder:
            # if it's coroutine function or normal function, call appropriately
            if asyncio.iscoroutinefunction(finder):
                return await finder(html)
            else:
                # run in executor if it might be CPU-bound / blocking
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, finder, html)
    except Exception:
        log.exception("Error while running find_direct_link_from_html")

    # Fallback minimal heuristic: search for common data.1024tera.com patterns
    try:
        # quick pass: unquote encoded HTML then search for 'data.' occurrences
        decoded = unquote(html or "")
        for token in ("data.1024tera.com", "d.1024tera.com", "/file/", "fid="):
            if token in decoded:
                # extract first http... token containing the token
                import re
                m = re.search(r"(https?://[^\s'\"<>]*" + re.escape(token.split(".")[0]) + r"[^\s'\"<>]*)", decoded, re.IGNORECASE)
                if m:
                    candidate = m.group(1)
                    return candidate
    except Exception:
        log.exception("Fallback extractor failed")

    return None


async def _notify_user_and_channels_on_error(client, message, user_url, err_text: str):
    """
    Notify the user (reply) and try to send a concise message to ERROR_CHANNEL.
    Failures here are logged and swallowed to avoid crashing the main flow.
    """
    try:
        # single user reply
        await message.reply(err_text, quote=True)
    except Exception:
        log.exception("Failed to reply to user with error")

    # notify ERROR_CHANNEL (best-effort)
    try:
        if hasattr(Config, "ERROR_CHANNEL") and Config.ERROR_CHANNEL:
            await client.send_message(Config.ERROR_CHANNEL,
                                      f"❌ ERROR\nUser: {getattr(message.from_user, 'id', 'unknown')}\nLink: {user_url}\nError: {err_text}")
    except Exception:
        log.warning("Failed to send to ERROR_CHANNEL (best-effort)")
