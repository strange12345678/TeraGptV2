# handlers/start.py
from pyrogram import filters
from pyrogram.types import Message
import logging
from config import Config
from Theinertbotz.database import db

log = logging.getLogger("TeraBoxBot")

START_TEXT = """<b>👋 Welcome to TeraBox Demo Downloader</b>

Send any TeraBox link and I'll fetch & download it for you.
I process links one-by-one to avoid API errors.
"""

def register_handlers(app):
    @app.on_message(filters.private & filters.command("start"))
    async def start_cmd(client, message: Message):
        try:
            uid = message.from_user.id
            db.add_user(uid)
            await message.reply(START_TEXT, parse_mode="html")
            log.info(f"/start from {uid}")
        except Exception as e:
            log.exception("start handler error")
