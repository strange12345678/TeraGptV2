from pyrogram import filters
from pyrogram.types import Message
from config import Config, logger
from script import Script
from Theinertbotz.engine import process_video
from Theinertbotz.utils import extract_links_from_message
import asyncio

def register_handlers(app):
    @app.on_message(filters.private & (filters.text | filters.caption))
    async def pm_handler(client, msg: Message):
        # ignore old messages (avoid replay on redeploy)
        import time
        if msg.date < (time.time() - Config.IGNORE_MESSAGE_AGE):
            logger.debug("Ignoring old message")
            return

        # get links from message (supports forwarded & caption & text & emojis)
        links = extract_links_from_message(msg)
        if not links:
            return  # no terabox links

        # if multiple links: process sequentially
        for link in links:
            logger.info(f"Processing link: {link} from user {msg.from_user.id}")
            res = await process_video(client, msg, link)
            # small delay between links to avoid API race
            await asyncio.sleep(1)
