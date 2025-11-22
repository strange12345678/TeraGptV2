# Theinertbotz/engine.py
import re
import asyncio
import logging
from urllib.parse import unquote
from Theinertbotz.api import fetch_play_html
from Theinertbotz.download import download_file
from Theinertbotz.uploader import upload_file
from config import Config
from Theinertbotz.database import db

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
        if any(d in u for d in ("d.1024tera.com", "data.1024tera.com", "1024tera.com", "terabox", "d.tera", "data.")):
            if any(k in u for k in ("fid=", "/file/", "fin=", "fn=")) or re.search(r"\.(mp4|mkv|mov|webm|mp3)(?:\?|$)", u, re.IGNORECASE):
                return True
        if "file" in u and ("sign=" in u or "expires=" in u or "fid=" in u):
            return True
        return False
    except Exception:
        return False

async def process_video(client, message, user_url: str):
    uid = getattr(message.from_user, "id", None)
    try:
        play_api_url = Config.TERAAPI_PLAY.format(url=user_url) if hasattr(Config, "TERAAPI_PLAY") else user_url
        log.info(f"Fetching play page via API: {play_api_url}")
        loop = asyncio.get_running_loop()
        # fetch HTML (fetch_play_html should be sync; run in executor)
        html = await loop.run_in_executor(None, fetch_play_html, user_url)
        log.info("Fetched play HTML in %.2fs (len=%d)", 0.0, len(html) if html else 0)  # placeholder timing if you want

        direct_link = await find_direct_link_from_html(html)

        if not direct_link:
            await message.reply("❌ Failed to extract direct link from play HTML.", quote=True)
            try:
                if getattr(Config, "ERROR_CHANNEL", None):
                    await client.send_message(Config.ERROR_CHANNEL, f"Failed to extract direct link for {user_url}\nPlay HTML length: {len(html) if html else 0}")
            except Exception:
                log.warning("Failed to send to ERROR_CHANNEL")
            return

        log.info(f"Found direct link: {direct_link}")

        # prepare bot username for ProgressManager
        me = await client.get_me()
        bot_username = "@" + me.username if getattr(me, "username", None) else (me.first_name or "@bot")

        # download -> upload -> store
        filepath, filename = await download_file(client, message, direct_link, bot_username, kind="download")

        # upload to user chat (send_video so Telegram treats as video)
        await upload_file(client, message, filepath, bot_username)

        # DB log (best-effort)
        try:
            if uid:
                db.add_log(uid, filename)
        except Exception:
            log.exception("db.add_log failed")

        # try backup to storage channel (best effort)
        try:
            if getattr(Config, "STORAGE_CHANNEL", None):
                await client.send_document(Config.STORAGE_CHANNEL, document=filepath, caption=f"Stored: {filename}")
        except Exception:
            log.warning("Failed to backup to STORAGE_CHANNEL")

        # send admin log
        try:
            if getattr(Config, "LOG_CHANNEL", None):
                await client.send_message(Config.LOG_CHANNEL, f"LOG: user={uid} text=Downloaded {filename}")
        except Exception:
            log.warning("Failed to send to LOG_CHANNEL")

    except Exception as e:
        log.exception("Processing error")
        try:
            await message.reply("❌ Processing error: " + str(e))
            if getattr(Config, "ERROR_CHANNEL", None):
                await client.send_message(Config.ERROR_CHANNEL, f"ERROR: {e}\nLink: {user_url}")
        except Exception:
            log.warning("Failed to notify ERROR_CHANNEL")
