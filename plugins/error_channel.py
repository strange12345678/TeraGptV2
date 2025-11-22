import logging
from config import Config
from pyrogram import enums

log = logging.getLogger("TeraBoxBot")

async def log_error(client, error_text: str):
    log.error(f"ERROR: {error_text}")
    if Config.ERROR_CHANNEL and Config.ERROR_CHANNEL != 0:
        try:
            msg = f"<b>❌ Error Report</b>\n<pre>{error_text}</pre>"
            await client.send_message(Config.ERROR_CHANNEL, msg, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            log.warning(f"Failed to send to ERROR_CHANNEL: {e}")
