import os
import logging

def _env_int(name, default=0):
    v = os.getenv(name, "")
    try:
        return int(v) if v != "" else default
    except:
        return default

class Config:
    API_ID = int(os.getenv("API_ID", 22582906))
    API_HASH = os.getenv("API_HASH", "e3096dde3e27c72a50e0e53d8ab23d6a")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8593002387:AAHDSfKf7VURo5HemGum4Nza-LmvqDBD8lU")

    # Optional channels (use -100... for groups)
    LOG_CHANNEL = _env_int("LOG_CHANNEL", -1003347866431)
    ERROR_CHANNEL = _env_int("ERROR_CHANNEL", -1003347866431)
    STORAGE_CHANNEL = _env_int("STORAGE_CHANNEL", -1003347866431)

    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
    IGNORE_MESSAGE_AGE = int(os.getenv("IGNORE_MESSAGE_AGE", 5))

# setup logging to stdout for Koyeb
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
)
logger = logging.getLogger("TeraBoxBot")
