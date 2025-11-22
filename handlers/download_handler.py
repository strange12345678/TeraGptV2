# handlers/download_handler.py
import re
import asyncio
import logging
from pyrogram import filters
from pyrogram.types import Message
from config import Config
from Theinertbotz.engine import process_video
from Theinertbotz.database import db

log = logging.getLogger("TeraBoxBot")

TERABOX_RE = re.compile(r"(https?://[^\s]+(?:terabox|1024terabox|terasharefile)[^\s]*)", re.IGNORECASE)

def extract_links(text: str):
    if not text:
        return []
    return TERABOX_RE.findall(text)

def register_handlers(app):
    @app.on_message(filters.private & ~filters.command("start"))
    async def main_handler(client, message: Message):
        try:
            text = message.text or message.caption or ""
            links = extract_links(text)
            if not links:
                await message.reply("No TeraBox link found. Send a valid link.")
                return

            # Process one by one (Option A)
            for link in links:
                log.info(f"Processing link: {link} from user {message.from_user.id}")
                await process_video(client, message, link.strip())
        except Exception as e:
            log.exception("main_handler error")
            try:
                await message.reply("Internal error while processing. Check logs.")
            except:
                pass
