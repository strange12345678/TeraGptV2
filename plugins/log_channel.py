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
        error_str = str(e)
        if "Peer id invalid" in error_str:
            log.error(f"Failed to send to LOG_CHANNEL {channel}: Bot is not in the channel or channel ID is invalid. Add bot as admin and try again.")
        elif "USER_RESTRICTED" in error_str or "CHAT_SEND_PLAIN_FORBIDDEN" in error_str:
            log.error(f"Failed to send to LOG_CHANNEL {channel}: Bot doesn't have permission to send messages. Check admin rights.")
        else:
            log.error(f"Failed to send to LOG_CHANNEL {channel}: {e}")
