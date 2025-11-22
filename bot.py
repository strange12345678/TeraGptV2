import os
from pyrogram import Client
from config import Config, logger
from core.router import register_all

os.makedirs("sessions", exist_ok=True)

app = Client(
    name="TeraBoxBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="sessions",
    workers=100,
    sleep_threshold=30
)

# register handlers
register_all(app)

logger.info("🔥 Pyrogram client initialized & handlers loaded!")
__all__ = ["app"]
