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
from plugins.premium_upload import upload_to_premium_channel

log = logging.getLogger("TeraBoxBot")

# ===== TERAAPI PATTERNS =====
# Patterns for TeraAPI (JSON/structured response format)
TERAAPI_JSON_RE = re.compile(r'"(?:url|downloadUrl|playUrl|directUrl|fileUrl|file_url)"\s*:\s*"(https?://[^"]+)"', re.IGNORECASE)
TERAAPI_JS_VAR_RE = re.compile(r"""(?:directUrl|direct_url|fastDownloadUrl|direct_link)\s*[:=]\s*["'](https?://[^"']+)["']""", re.IGNORECASE)

# ===== ITERAPLAY PATTERNS =====
# Patterns for iTeraPlay (HTML with embedded JavaScript)
ITERAPLAY_WINDOW_RE = re.compile(r'window\.(?:playurl|downloadurl|directurl|fileurl|url)\s*=\s*["\']?(https?://[^"\'\s;]+)', re.IGNORECASE)
ITERAPLAY_SRC_RE = re.compile(r'(?:src|data-url|data-src)\s*=\s*["\']?(https?://[^"\'\s>]+)', re.IGNORECASE)

# ===== GENERIC PATTERNS (fallback for both) =====
CANDIDATE_RE = re.compile(
    r"https?://(?:d|data|file|data\.)[^\s'\"<>]+(?:/file/|/file\-|/file%2F|/file%3F|/file\?)[^\s'\"<>]*",
    re.IGNORECASE
)
GENERIC_URL_RE = re.compile(
    r"https?://[^\s'\"<>]+(?:d\.1024tera\.com|data\.1024tera\.com|1024tera\.com|data\.)[^\s'\"<>]*",
    re.IGNORECASE
)
HREF_RE = re.compile(r'href=["\'](https?://[^"\']+)["\']', re.IGNORECASE)
URL_ANY_RE = re.compile(r"https?://[^\s'\"<>]+")

async def extract_teraapi_link(html: str):
    """Extract link from TeraAPI response (JSON/structured format)"""
    log.debug("Using TeraAPI extractor")
    
    # 1) JSON format with quoted URLs
    for m in TERAAPI_JSON_RE.findall(html):
        if m and is_plausible_direct(m):
            log.info(f"TeraAPI: Found via JSON_RE: {m[:80]}")
            return m
    
    # 2) JS variable format
    for m in TERAAPI_JS_VAR_RE.findall(html):
        if m and is_plausible_direct(m):
            log.info(f"TeraAPI: Found via JS_VAR_RE: {m[:80]}")
            return m
    
    # 3) Candidate patterns
    for c in CANDIDATE_RE.findall(html):
        if is_plausible_direct(c):
            log.info(f"TeraAPI: Found via CANDIDATE_RE: {c[:80]}")
            return c
    
    # 4) Generic patterns
    for c in GENERIC_URL_RE.findall(html):
        if is_plausible_direct(c):
            log.info(f"TeraAPI: Found via GENERIC_RE: {c[:80]}")
            return c
    
    return None

async def extract_iteraplay_link(html: str):
    """Extract link from iTeraPlay response (HTML with embedded JavaScript)"""
    log.debug("Using iTeraPlay extractor")
    
    # 1) Window variables (primary for iTeraPlay)
    for m in ITERAPLAY_WINDOW_RE.findall(html):
        if m and is_plausible_direct(m):
            log.info(f"iTeraPlay: Found via WINDOW_RE: {m[:80]}")
            return m
    
    # 2) src= and data-url= attributes
    for m in ITERAPLAY_SRC_RE.findall(html):
        if m and is_plausible_direct(m):
            log.info(f"iTeraPlay: Found via SRC_RE: {m[:80]}")
            return m
    
    # 3) Try generic patterns as fallback
    for c in CANDIDATE_RE.findall(html):
        if is_plausible_direct(c):
            log.info(f"iTeraPlay: Found via CANDIDATE_RE: {c[:80]}")
            return c
    
    for c in GENERIC_URL_RE.findall(html):
        if is_plausible_direct(c):
            log.info(f"iTeraPlay: Found via GENERIC_RE: {c[:80]}")
            return c
    
    return None

async def find_direct_link_from_html(html: str, api_source: str = "teraapi"):
    """
    Extract direct link from HTML based on API source.
    Uses optimized patterns for each API type.
    """
    log.debug(f"Searching for download link using {api_source} extractor (HTML length: {len(html)})")
    
    if api_source == "iteraplay":
        direct_link = await extract_iteraplay_link(html)
    else:  # teraapi or unknown
        direct_link = await extract_teraapi_link(html)
    
    # Final fallback: try generic URL extraction if specific extractors failed
    if not direct_link:
        log.debug(f"Extractors failed, trying generic fallback...")
        for u in URL_ANY_RE.findall(html):
            if any(x in u for x in ("d.1024", "data.1024", "fid=", "/file/")) and is_plausible_direct(u):
                log.info(f"Found via generic URL_ANY_RE: {u[:80]}")
                direct_link = u
                break
        
        # Try decoded version
        if not direct_link:
            decoded = unquote(html)
            for u in URL_ANY_RE.findall(decoded):
                if any(x in u for x in ("d.1024", "data.1024", "fid=", "/file/")) and is_plausible_direct(u):
                    log.info(f"Found via decoded URL_ANY_RE: {u[:80]}")
                    direct_link = u
                    break
    
    if not direct_link:
        log.warning(f"No download link found using {api_source} extractor. HTML length: {len(html)}")
    
    return direct_link

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

async def process_video(client, message, user_url: str) -> None:
    from typing import Optional
    uid: Optional[int] = getattr(message.from_user, "id", None)
    username: str = getattr(message.from_user, "username", "Unknown") or "Unknown"
    filename: Optional[str] = None
    filepath: Optional[str] = None
    
    try:
        log.info(f"Processing link: {user_url} from user {uid}")
        loop = asyncio.get_running_loop()
        html, api_source = await loop.run_in_executor(None, fetch_play_html, user_url)
        log.info(f"Fetched play HTML using {api_source} (len={len(html) if html else 0})")

        direct_link = await find_direct_link_from_html(html, api_source)

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
        
        # Get file size
        file_size = human_size(os.path.getsize(filepath)) if os.path.exists(filepath) else "Unknown"

        # Generate thumbnail for video files
        thumb_path = None
        if filename and filename.lower().endswith(('.mp4', '.mkv', '.mov', '.webm')):
            thumb_path = generate_thumbnail(filepath)

        # upload to user chat with thumbnail
        await upload_file(client, message, filepath, bot_username)

        # DB log
        try:
            if uid:
                db.add_log(uid, filename)
        except Exception:
            log.exception("db.add_log failed")

        # Backup to storage channel with thumbnail
        try:
            await backup_file(client, filepath, filename, file_size, username, user_url)
        except Exception:
            log.exception("Failed to backup to STORAGE_CHANNEL")
        
        # Auto-upload to premium channel for premium users
        try:
            if uid:
                await upload_to_premium_channel(client, filepath, filename, file_size, uid, username)
        except Exception:
            log.exception("Failed to upload to PREMIUM_UPLOAD_CHANNEL")
            
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
