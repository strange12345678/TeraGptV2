from pyrogram import Client
from config import Config, logger
import os

# ensure sessions folder exists
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

logger.info("Pyrogram client initialized")
