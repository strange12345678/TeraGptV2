import logging
from config import Config
from pyrogram import enums

log = logging.getLogger("TeraBoxBot")

async def backup_file(client, path: str, file_name: str, file_size: str, user: str, link: str) -> None:
    log.info(f"STORAGE: backup request {file_name} {file_size}")
    channel = Config.STORAGE_CHANNEL
    if not channel or channel == 0:
        return
    try:
        caption = f"<b>📂 File:</b> <code>{file_name}</code>\n<b>📊 Size:</b> {file_size}\n<b>👤 User:</b> @{user}\n<b>🔗 Link:</b> <code>{link}</code>"
        await client.send_document(channel, document=path, caption=caption, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        log.warning(f"Failed to backup to STORAGE_CHANNEL: {e}")
