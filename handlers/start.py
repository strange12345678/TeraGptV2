from pyrogram import filters
from config import Config, logger
from script import Script

def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(client, msg):
        logger.info(f"/start from {msg.from_user.id}")
        await msg.reply(Script.START)
