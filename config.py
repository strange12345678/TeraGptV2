# config.py
import os

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8593002387:AAHDSfKf7VURo5HemGum4Nza-LmvqDBD8lU")
    API_ID = int(os.getenv("API_ID", "22582906"))
    API_HASH = os.getenv("API_HASH", "e3096dde3e27c72a50e0e53d8ab23d6a")

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://testhubpro7:Q7iFC6EYg9URONBN@cluster0.0neghuj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB = os.getenv("MONGO_DB", "teraboxbot")

    # Channels - must be numeric ids (e.g. -1001234567890)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1003347866431"))
    ERROR_CHANNEL = int(os.getenv("ERROR_CHANNEL", "-1003347866431"))
    STORAGE_CHANNEL = int(os.getenv("STORAGE_CHANNEL", "-1003347866431"))

    # Only the play endpoint (the only reliable one you said)
    TERAAPI_PLAY = "https://teraapi.boogafantastic.workers.dev/play?url={url}"

    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
    WORKERS = int(os.getenv("WORKERS", "20"))
