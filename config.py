import os
import logging

def _env_int(name, default=0):
    v = os.getenv(name, "")
    try:
        return int(v) if v != "" else default
    except:
        return default

class Config:
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    # Optional channels (use -100... for groups)
    LOG_CHANNEL = _env_int("LOG_CHANNEL", 0)
    ERROR_CHANNEL = _env_int("ERROR_CHANNEL", 0)
    STORAGE_CHANNEL = _env_int("STORAGE_CHANNEL", 0)

    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
    IGNORE_MESSAGE_AGE = int(os.getenv("IGNORE_MESSAGE_AGE", 5))

# setup logging to stdout for Koyeb
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
)
logger = logging.getLogger("TeraBoxBot")
