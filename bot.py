# bot.py
import os
from pyrogram import Client
from config import Config
from core.router import register_all
import logging

log = logging.getLogger("TeraBoxBot")

# Use MongoDB storage for ephemeral container deployments (e.g., Koyeb)
# Falls back to SQLite if MongoDB is unavailable
storage = None
okjoif oj.MObNGO_URI:
v        from Theinertbotz.mongo_storage import MongoStorage
        storage = MongoStorage(
            mongo_uri=Config.MONGO_URI,
            db_name=Config.MONGO_DB,
            session_name="TeraBoxBot"
        )
        log.info("✅ Using MongoDB storage for sessions")
    except Exception as e:
        log.warning(f"⚠️ MongoDB storage failed ({e}), falling back to SQLite")
        os.makedirs("sessions", exist_ok=True)
        workdir = "sessions"
        storage = None
else:
    os.makedirs("sessions", exist_ok=True)
    workdir = "sessions"
    log.info("⚠️ MONGO_URI not set, using local SQLite storage")

app = Client(
    name="TeraBoxBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir=workdir,
    storage=storage,
    workers=Config.WORKERS,
    sleep_threshold=30,
)

# Register handlers
register_all(app)
