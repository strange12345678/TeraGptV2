# Theinertbotz/engine.py
import re
import asyncio
import logging
import os
from urllib.parse import unquote
from pyrogram import enums
from Theinertbotz.api import fetch_play_html
from Theinertbotz.download import download_file
from Theinertbotz.uploader import upload_file
from Theinertbotz.thumbnail import generate_thumbnail
from Theinertbotz.processing import human_size
from config import Config
from Theinertbotz.database import db
from plugins.log_channel import log_action
from plugins.error_channel import log_error
from plugins.storage_channel import backup_file

log = logging.getLogger("TeraBoxBot")

# Patterns tuned to common tera/play html outputs
CANDIDATE_RE = re.compile(
    r"https?://(?:d|data|file|data\.)[^\s'\"<>]+(?:/file/|/file\-|/file%2F|/file%3F|/file\?)[^\s'\"<>]*",
    re.IGNORECASE
)

GENERIC_URL_RE = re.compile(
    r"https?://[^\s'\"<>]+(?:d\.1024tera\.com|data\.1024tera\.com|1024tera\.com|data\.)[^\s'\"<>]*",
    re.IGNORECASE
)

JS_QUOTE_RE = re.compile(r"""(?:(?:directUrl|direct_url|fastDownloadUrl|direct_link)\s*[:=]\s*["'](https?://[^"']+)["'])""", re.IGNORECASE)
HREF_RE = re.compile(r'href=["\'](https?://[^"\']+)["\']', re.IGNORECASE)
URL_ANY_RE = re.compile(r"https?://[^\s'\"<>]+")

async def find_direct_link_from_html(html: str):
    # 1) JS variable directUrl
    for m in JS_QUOTE_RE.findall(html):
        url = m
        if url and is_plausible_direct(url):
            return url

    cand = CANDIDATE_RE.findall(html)
    if cand:
        for c in cand:
            if is_plausible_direct(c):
                return c

    cand2 = GENERIC_URL_RE.findall(html)
    if cand2:
        for c in cand2:
            if is_plausible_direct(c):
                return c

    for m in HREF_RE.findall(html):
        if is_plausible_direct(m):
            return m

    for u in URL_ANY_RE.findall(html):
        if any(x in u for x in ("d.1024", "data.1024", "fid=", "/file/")) and is_plausible_direct(u):
            return u

    decoded = unquote(html)
    for u in URL_ANY_RE.findall(decoded):
        if any(x in u for x in ("d.1024", "data.1024", "fid=", "/file/")) and is_plausible_direct(u):
            return u

    return None

def is_plausible_direct(url: str) -> bool:
    try:
        u = url.strip()
        if not u.startswith("http"):
            return False
        # Check for TeraBox-related domains
        if any(d in u for d in ("d.1024tera.com", "data.1024tera.com", "1024tera.com", "terabox", "terasharefile", "tera.co", "d.tera", "data.", "mirrobox", "nephobox", "freeterabox", "4funbox", "terabox.app", "terabox.fun", "momerybox", "teraboxapp", "tibibox")):
            if any(k in u for k in ("fid=", "/file/", "fin=", "fn=")) or re.search(r"\.(mp4|mkv|mov|webm|mp3)(?:\?|$)", u, re.IGNORECASE):
                return True
        if "file" in u and ("sign=" in u or "expires=" in u or "fid=" in u):
            return True
        return False
    except Exception:
        return False

async def process_video(client, message, user_url: str, status_msg=None) -> None:
    from typing import Optional
    uid: Optional[int] = getattr(message.from_user, "id", None)
    username: str = getattr(message.from_user, "username", "Unknown") or "Unknown"
    filename: Optional[str] = None
    filepath: Optional[str] = None
    
    try:
        play_api_url = Config.TERAAPI_PLAY.format(url=user_url) if hasattr(Config, "TERAAPI_PLAY") else user_url
        log.info(f"Processing link: {user_url} from user {uid}")
        loop = asyncio.get_running_loop()
        html = await loop.run_in_executor(None, fetch_play_html, user_url)
        log.info(f"Fetched play HTML (len={len(html) if html else 0})")

        direct_link = await find_direct_link_from_html(html)

        if not direct_link:
            error_msg = f"Failed to extract direct link for {user_url}"
            await message.reply("❌ Failed to extract direct link from play HTML.", quote=True)
            await log_error(client, error_msg)
            return

        log.info(f"Found direct link: {direct_link}")

        # prepare bot username for ProgressManager
        me = await client.get_me()
        bot_username = "@" + me.username if getattr(me, "username", None) else (me.first_name or "@bot")

        # download -> upload -> store
        filepath, filename = await download_file(client, message, direct_link, bot_username, kind="download")
        
        # Keep original filename for video detection before renaming
        original_filename = filename
        
        # Get file size
        file_size = human_size(os.path.getsize(filepath)) if os.path.exists(filepath) else "Unknown"

        # Generate thumbnail for video files
        thumb_path = None
        if filename and filename.lower().endswith(('.mp4', '.mkv', '.mov', '.webm')):
            thumb_path = generate_thumbnail(filepath)

        # upload to user chat with thumbnail - pass original filename for correct video detection
        await upload_file(client, message, filepath, bot_username, original_filename=original_filename)

        # DB log
        try:
            if uid:
                db.add_log(uid, filename)
        except Exception:
            log.exception("db.add_log failed")

        # Backup to storage channel with thumbnail - pass original filename for video detection
        try:
            # Extract original filename from direct_link or use filename
            original_name = filename.split('_')[-1] if '_' in filename else filename
            await backup_file(client, filepath, filename, file_size, username, user_url, uid, original_name)
        except Exception:
            log.exception("Failed to backup to STORAGE_CHANNEL")

        # Clean up thumbnail if exists
        if thumb_path and os.path.exists(thumb_path):
            try:
                os.remove(thumb_path)
            except:
                pass
        
        # Auto-delete downloaded file if enabled
        if db.is_auto_delete_enabled():
            try:
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)
                    log.info(f"Auto-deleted file: {filename}")
            except Exception as e:
                log.error(f"Failed to auto-delete {filename}: {e}")

    except Exception as e:
        log.exception("Processing error")
        error_text = f"ERROR: {str(e)}\nLink: {user_url}\nUser: {uid}"
        try:
            # Show clean error to user without API URL
            await message.reply(f"❌ Processing Error: Failed to process file. Please try again.\n\n🔗 Link: {user_url}")
        except:
            pass
        try:
            await log_error(client, error_text)
        except Exception:
            log.warning("Failed to notify ERROR_CHANNEL")
