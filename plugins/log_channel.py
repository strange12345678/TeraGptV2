import logging
from config import Config
from pyrogram import enums

log = logging.getLogger("TeraBoxBot")

async def log_action(client, user_id: int, text: str) -> None:
    log.info(f"LOG: user={user_id} text={text}")
    channel = Config.LOG_CHANNEL
    if not channel or channel == 0:
        return
    try:
        msg = f"<b>#Action</b>\n<b>User:</b> <code>{user_id}</code>\n{text}"
        await client.send_message(channel, msg, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        log.warning(f"Failed to send to LOG_CHANNEL: {e}")
