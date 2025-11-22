import logging
from config import Config
from pyrogram import enums

log = logging.getLogger("TeraBoxBot")

async def log_error(client, error_text: str) -> None:
    log.error(f"ERROR: {error_text}")
    channel = Config.ERROR_CHANNEL
    if not channel or channel == 0:
        log.debug(f"ERROR_CHANNEL not configured, skipping error log")
        return
    try:
        msg = f"<b>❌ Error Report</b>\n<pre>{error_text}</pre>"
        await client.send_message(chat_id=channel, text=msg, parse_mode=enums.ParseMode.HTML)
        log.debug(f"Error sent to channel {channel}")
    except Exception as e:
        log.error(f"Failed to send to ERROR_CHANNEL {channel}: {e}")
