from pyrogram import filters
from pyrogram.types import Message
from config import Config, logger
from Theinertbotz.utils import extract_links_from_message
from Theinertbotz.engine import process_video
import asyncio
import time

def register_handlers(app):
    @app.on_message(filters.private & (filters.text | filters.caption))
    async def pm_handler(client, msg: Message):
        # ignore old messages (convert datetime to timestamp)
        try:
            msg_ts = msg.date.timestamp()
            if msg_ts < (time.time() - Config.IGNORE_MESSAGE_AGE):
                logger.debug("Ignoring old message (too old)")
                return
        except Exception:
            pass

        links = extract_links_from_message(msg)
        if not links:
            return

        for link in links:
            logger.info(f"Processing link: {link} from user {msg.from_user.id}")
            await process_video(client, msg, link)
            await asyncio.sleep(1)  # small delay between links
