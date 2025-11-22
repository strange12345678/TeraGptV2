from config import Config, logger
from script import Script
from typing import Any

async def log_error(client: Any, error_text: str):
    logger.error(f"ERROR: {error_text}")
    if Config.ERROR_CHANNEL:
        try:
            await client.send_message(Config.ERROR_CHANNEL, f"❌ Error:\n<pre>{error_text}</pre>")
        except Exception as e:
            logger.warning(f"Failed to send to ERROR_CHANNEL: {e}")
