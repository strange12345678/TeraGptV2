from pyrogram import filters
from script import Script
from config import logger

def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(_, msg):
        logger.info(f"/start from {msg.from_user.id}")
        await msg.reply(Script.START)
