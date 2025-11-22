import logging
from config import Config
from pyrogram import enums

log = logging.getLogger("TeraBoxBot")

async def log_error(client, error_text: str) -> None:
    log.error(f"ERROR: {error_text}")
    channel = Config.ERROR_CHANNEL
    if not channel or channel == 0:
        return
    try:
        msg = f"<b>❌ Error Report</b>\n<pre>{error_text}</pre>"
        await client.send_message(channel, msg, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        log.warning(f"Failed to send to ERROR_CHANNEL: {e}")
