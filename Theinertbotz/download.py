from pyrogram import filters
from pyrogram.types import Message
from config import Config, logger
from script import Script
from Theinertbotz.engine import process_video
from Theinertbotz.utils import extract_links_from_message
import asyncio
import time

def register_handlers(app):
    @app.on_message(filters.private & (filters.text | filters.caption))
    async def pm_handler(client, msg: Message):

        # ---- FIX: datetime vs float comparison ----
        msg_ts = msg.date.timestamp()  # convert datetime -> float
        if msg_ts < (time.time() - Config.IGNORE_MESSAGE_AGE):
            logger.debug("Ignoring old message (too old)")
            return

        # ---- Extract links ----
        links = extract_links_from_message(msg)
        if not links:
            return

        # ---- Process each link sequentially ----
        for link in links:
            logger.info(f"Processing link: {link} from user {msg.from_user.id}")
            await process_video(client, msg, link)
            await asyncio.sleep(1)
