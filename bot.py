# bot.py
import os
from pyrogram import Client
from config import Config
from core.router import register_all
import logging

log = logging.getLogger("TeraBoxBot")

os.makedirs("sessions", exist_ok=True)

app = Client(
    name="TeraBoxBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="sessions",
    workers=Config.WORKERS,
    sleep_threshold=30,
)

# Register handlers
register_all(app)
