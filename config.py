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
    PREMIUM_UPLOAD_CHANNEL = int(os.getenv("PREMIUM_UPLOAD_CHANNEL", "0")) if os.getenv("PREMIUM_UPLOAD_CHANNEL") else None

    # Only the play endpoint (the only reliable one you said)
    TERAAPI_PLAY = "https://teraapi.boogafantastic.workers.dev/play?url={url}"

    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
    WORKERS = int(os.getenv("WORKERS", "20"))
    
    # Auto-rename pattern: "timestamp", "datetime", or "" (disabled)
    # Default is disabled - only apply if user explicitly sets it
    AUTO_RENAME = os.getenv("AUTO_RENAME", "")
    
    # Admin user IDs (comma-separated)
    ADMIN_IDS = []
    admin_str = os.getenv("ADMIN_IDS", "")
    if admin_str:
        ADMIN_IDS = [int(uid.strip()) for uid in admin_str.split(",") if uid.strip()]
    
    # Auto-delete downloaded files after upload
    AUTO_DELETE = os.getenv("AUTO_DELETE", "True").lower() == "true"
    
    # Daily download limit for free users
    DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", "5"))
    
    # Premium QR Code image URL
    QR_CODE = "https://i.ibb.co/hFjZ6CWD/photo-2025-08-10-02-24-51-7536777335068950548.jpg"
    
    # Start page image
    START_IMG = "https://i.ibb.co/TBH7WZGs/photo-2025-11-23-03-01-55-7575750765961019396.jpg"
