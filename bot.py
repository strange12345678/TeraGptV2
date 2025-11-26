# bot.py
import os
import asyncio
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

# Startup event to resolve channels
_channels_resolved = False

@app.on_start()
async def resolve_channels_on_start():
    """Resolve all configured channel peers when bot starts"""
    global _channels_resolved
    if _channels_resolved:
        return
    _channels_resolved = True
    
    channels = {
        "LOG_CHANNEL": Config.LOG_CHANNEL,
        "ERROR_CHANNEL": Config.ERROR_CHANNEL,
        "STORAGE_CHANNEL": Config.STORAGE_CHANNEL,
        "PREMIUM_UPLOAD_CHANNEL": Config.PREMIUM_UPLOAD_CHANNEL,
    }
    
    log.info("🔄 Resolving configured channels on startup...")
    for name, channel_id in channels.items():
        if not channel_id or channel_id == 0:
            log.debug(f"{name} not configured, skipping")
            continue
        try:
            chat = await app.get_chat(channel_id)
            title = chat.title if hasattr(chat, 'title') else 'Unknown'
            log.info(f"✅ {name} resolved: {title} ({channel_id})")
        except Exception as e:
            log.error(f"❌ {name} ({channel_id}) failed to resolve: {e}")
            log.error(f"   Make sure bot is added as ADMIN to this channel")
