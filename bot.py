# bot.py

import os
from pyrogram import Client
from config import Config, logger
from handlers import register_all

# ---------------------------------------------------------
# Ensure sessions directory exists for Pyrogram state files
# ---------------------------------------------------------
os.makedirs("sessions", exist_ok=True)

# ---------------------------------------------------------
# Initialize bot client
# ---------------------------------------------------------
app = Client(
    name="TeraBoxBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="sessions",
    workers=200,                 # High performance
    sleep_threshold=30,          # Prevent API flooding
    in_memory=False              # Required for Koyeb restarts
)

# ---------------------------------------------------------
# Register ALL handlers (start + download handler)
# ---------------------------------------------------------
register_all(app)

logger.info("🔥 Pyrogram client initialized & handlers loaded!")

# ---------------------------------------------------------
# Export app
# ---------------------------------------------------------
__all__ = ["app"]
