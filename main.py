# main.py
import logging
import threading
import asyncio
from pyrogram import filters
from bot import app
from health import create_health_app
from config import Config
from plugins.log_channel import log_action

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
log = logging.getLogger("TeraBoxBot")

R_LOG_TXT = """<u><b>🚀{bot_name} Restarted</b></u>

<b>Status: 🟢 Online
Version: 2.1
Time Zone: Asia/Kolkata</b>"""

_startup_done = False

async def send_startup_message():
    """Send startup notification to log channel"""
    global _startup_done
    if _startup_done:
        return
    _startup_done = True
    
    try:
        await asyncio.sleep(1.5)  # Wait for bot to be fully ready
        me = await app.get_me()
        bot_username = "@" + me.username if getattr(me, "username", None) else "TeraBox Bot"
        msg = R_LOG_TXT.format(bot_name=bot_username)
        await log_action(app, None, msg)
        log.info("✅ Startup message sent to LOG_CHANNEL")
    except Exception as e:
        log.error(f"Could not send startup message: {e}")

@app.on_message(filters.private)
async def first_message_handler(client, message):
    """Trigger startup log on first message"""
    global _startup_done
    if not _startup_done:
        asyncio.create_task(send_startup_message())

def run_bot():
    log.info("🔥 Pyrogram client initialized & handlers loaded!")
    
    # Schedule startup message in a background task
    def schedule_startup():
        asyncio.run(send_startup_message())
    
    # Run startup in a separate thread after a delay
    startup_thread = threading.Thread(target=lambda: (asyncio.sleep(2), schedule_startup()), daemon=True)
    
    # Actually, simpler - just run app and let handler catch it
    app.run()
