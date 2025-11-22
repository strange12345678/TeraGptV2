from config import Config, logger
from script import Script
from typing import Any

async def log_action(client: Any, user_id: int, text: str):
    # log to console
    logger.info(f"LOG: user={user_id} text={text}")
    # optional channel
    if Config.LOG_CHANNEL:
        try:
            await client.send_message(Config.LOG_CHANNEL, Script.START + f"\n\nUser: {user_id}\n{text}")
        except Exception as e:
            logger.warning(f"Failed to send LOG_CHANNEL message: {e}")
