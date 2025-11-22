import logging
from typing import Optional
from config import Config
from pyrogram import enums

log = logging.getLogger("TeraBoxBot")

async def log_action(client, user_id: Optional[int], text: str) -> None:
    log.info(f"LOG: user={user_id} text={text}")
    channel = Config.LOG_CHANNEL
    if not channel or channel == 0:
        log.debug(f"LOG_CHANNEL not configured, skipping log")
        return
    try:
        uid_str = str(user_id) if user_id else "Unknown"
        msg = f"<b>#Action</b>\n<b>User:</b> <code>{uid_str}</code>\n{text}"
        await client.send_message(chat_id=channel, text=msg, parse_mode=enums.ParseMode.HTML)
        log.debug(f"Log sent to channel {channel}")
    except Exception as e:
        log.error(f"Failed to send to LOG_CHANNEL {channel}: {e}")
