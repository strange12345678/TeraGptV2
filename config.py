# config.py
import os
import logging

logger = logging.getLogger("TeraBoxBot")

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID", "0")) if os.getenv("API_ID") else None
    API_HASH = os.getenv("API_HASH")

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB", "teraboxbot")

    # Channels - must be numeric ids (e.g. -1001234567890)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0")) if os.getenv("LOG_CHANNEL") else None
    ERROR_CHANNEL = int(os.getenv("ERROR_CHANNEL", "0")) if os.getenv("ERROR_CHANNEL") else None
    STORAGE_CHANNEL = int(os.getenv("STORAGE_CHANNEL", "0")) if os.getenv("STORAGE_CHANNEL") else None

    # Only the play endpoint (the only reliable one you said)
    TERAAPI_PLAY = "https://teraapi.boogafantastic.workers.dev/play?url={url}"

    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
    WORKERS = int(os.getenv("WORKERS", "20"))
