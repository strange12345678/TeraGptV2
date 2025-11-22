from config import Config, logger
from script import Script

async def log_action(client, user_id: int, text: str):
    logger.info(f"LOG: user={user_id} text={text}")
    if Config.LOG_CHANNEL:
        try:
            await client.send_message(Config.LOG_CHANNEL, f"#NewAction\nUser: {user_id}\n{text}")
        except Exception as e:
            logger.warning(f"Failed to send to LOG_CHANNEL: {e}")
