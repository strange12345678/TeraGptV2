# main.py
import logging
import threading
import asyncio
from bot import app
from health import create_health_app
from config import Config
from plugins.log_channel import log_action

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
log = logging.getLogger("TeraBoxBot")

R_LOG_TXT = """<u><b>🚀 TeraBox Bot Restarted</b></u>

<b>Status: 🟢 Online
Version: 2.1
Time Zone: Asia/Kolkata</b>"""

async def send_startup_message():
    """Send startup notification to log channel"""
    try:
        me = await app.get_me()
        bot_username = "@" + me.username if getattr(me, "username", None) else "TeraBox Bot"
        msg = R_LOG_TXT.replace("TeraBox Bot", bot_username)
        await log_action(app, None, msg)
        log.info("✅ Startup message sent to LOG_CHANNEL")
    except Exception as e:
        log.warning(f"Could not send startup message: {e}")

def run_bot():
    log.info("🔥 Pyrogram client initialized & handlers loaded!")
    # Schedule startup message
    app.add_handler(
        __import__('pyrogram').filters.command("startup"),
        lambda c, m: send_startup_message()
    )
    # Send startup message when client connects
    app.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_startup_message())
    app.stop()

if __name__ == "__main__":
    # Start health server (Flask) in background thread
    health_app = create_health_app()
    t = threading.Thread(target=lambda: health_app.run(host="0.0.0.0", port=8000), daemon=True)
    t.start()

    run_bot()
