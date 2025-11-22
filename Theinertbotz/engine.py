# Theinertbotz/engine.py
import re
import asyncio
import logging
from urllib.parse import unquote, urlparse, parse_qs
from Theinertbotz.api import fetch_play_html
from Theinertbotz.download import download_file
from Theinertbotz.uploader import upload_file
from config import Config
from Theinertbotz.database import db

log = logging.getLogger("TeraBoxBot")

# Patterns tuned to common tera/play html outputs
# look for d.1024tera.com or data.1024tera.com or data.*file paths
CANDIDATE_RE = re.compile(
    r"https?://(?:d|data|file|data\.)[^\s'\"<>]+(?:/file/|/file\-|/file%2F|/file%3F|/file\?)[^\s'\"<>]*",
    re.IGNORECASE
)

GENERIC_URL_RE = re.compile(
    r"https?://[^\s'\"<>]+(?:d\.1024tera\.com|data\.1024tera\.com|1024tera\.com|data\.)[^\s'\"<>]*",
    re.IGNORECASE
)

# look for JS variable assignments like: const directUrl = "https://data.1024tera.com/..."
JS_QUOTE_RE = re.compile(r"""(?:(?:directUrl|direct_url|fastDownloadUrl|direct_link)\s*[:=]\s*["'](https?://[^"']+)["'])""", re.IGNORECASE)

# href="https://data.1024tera.com/..." or <a ... data-download="...">
HREF_RE = re.compile(r'href=["\'](https?://[^"\']+)["\']', re.IGNORECASE)

# find urls wherever
URL_ANY_RE = re.compile(r"https?://[^\s'\"<>]+")

async def find_direct_link_from_html(html: str):
    """
    Try multiple heuristics to extract a direct-download URL from the returned play HTML.
    Returns the first plausible URL or None.
    """
    # 1) JS variable directUrl / fastDownloadUrl
    for m in JS_QUOTE_RE.findall(html):
        url = m
        if url and is_plausible_direct(url):
            return url

    # 2) Candidate pattern (d. | data. file patterns)
    cand = CANDIDATE_RE.findall(html)
    if cand:
        for c in cand:
            if is_plausible_direct(c):
                return c

    # 3) Generic 1024/data host matches
    cand2 = GENERIC_URL_RE.findall(html)
    if cand2:
        for c in cand2:
            if is_plausible_direct(c):
                return c

    # 4) href attributes with d.* or data.* hosts
    for m in HREF_RE.findall(html):
        if is_plausible_direct(m):
            return m

    # 5) fallback: any URL that contains 'file' or 'fid=' or 'd.' and looks like direct
    for u in URL_ANY_RE.findall(html):
        if any(x in u for x in ("d.1024", "data.1024", "fid=", "/file/")) and is_plausible_direct(u):
            return u

    # 6) unquote and try again (sometimes it's url-encoded)
    decoded = unquote(html)
    for u in URL_ANY_RE.findall(decoded):
        if any(x in u for x in ("d.1024", "data.1024", "fid=", "/file/")) and is_plausible_direct(u):
            return u

    return None

def is_plausible_direct(url: str) -> bool:
    """
    Quick heuristics to accept/reject a candidate direct url.
    """
    try:
        u = url.strip()
        # must be http(s)
        if not u.startswith("http"):
            return False
        # must contain domain we trust
        if any(d in u for d in ("d.1024tera.com", "data.1024tera.com", "1024tera.com", "terabox", "d.tera", "data.")):
            # avoid scripts or .m3u8 that are not direct mp4 (we may still allow m3u8)
            # Accept if it contains 'fid=' or '/file/' or 'fin=' or 'fn=' or ends with typical media extension
            if any(k in u for k in ("fid=", "/file/", "fin=", "fn=")) or re.search(r"\.(mp4|mkv|mov|webm|mp3)(?:\?|$)", u, re.IGNORECASE):
                return True
        # last chance: if it contains 'file' and has many params -> likely direct link
        if "file" in u and ("sign=" in u or "expires=" in u or "fid=" in u):
            return True
        return False
    except Exception:
        return False

async def process_video(client, message, user_url: str):
    uid = message.from_user.id
    try:
        play_api_url = Config.TERAAPI_PLAY.format(url=user_url)
        log.info(f"Fetching play page via API: {play_api_url}")
        loop = asyncio.get_event_loop()
        # fetch HTML synchronously in thread (requests)
        html = await loop.run_in_executor(None, fetch_play_html, user_url)

        # try to extract direct link
        direct_link = await find_direct_link_from_html(html)

        if not direct_link:
            # Try to parse filename or streaming info to send better error
            await message.reply("❌ Failed to extract direct link from play HTML.", quote=True)
            try:
                await client.send_message(Config.ERROR_CHANNEL, f"Failed to extract direct link for {user_url}\nPlay HTML length: {len(html)}")
            except Exception:
                log.warning("Failed to send to ERROR_CHANNEL")
            return

        log.info(f"Found direct link: {direct_link}")

        # download -> upload -> store
        me = await client.get_me()
        bot_username = "@" + me.username if me.username else me.first_name

        filepath, filename = await download_file(client, message, direct_link, bot_username)

        # upload to user chat (send_video so Telegram treats as video)
        await upload_file(client, message, filepath, bot_username)

        # DB log
        db.add_log(uid, filename)

        # try backup to storage channel (best effort)
        try:
            await client.send_document(Config.STORAGE_CHANNEL, document=filepath, caption=f"Stored: {filename}")
        except Exception:
            log.warning("Failed to backup to STORAGE_CHANNEL")

        # send admin log
        try:
            await client.send_message(Config.LOG_CHANNEL, f"LOG: user={uid} text=Downloaded {filename}")
        except Exception:
            log.warning("Failed to send to LOG_CHANNEL")

    except Exception as e:
        log.exception("Processing error")
        try:
            await message.reply("❌ Processing error: " + str(e))
            await client.send_message(Config.ERROR_CHANNEL, f"ERROR: {e}\nLink: {user_url}")
        except Exception:
            log.warning("Failed to notify ERROR_CHANNEL")
