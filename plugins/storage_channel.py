from config import Config, logger

async def backup_file(client, path: str, file_name: str, file_size: str, user: str, link: str):
    logger.info(f"STORAGE: backup request {file_name} {file_size}")
    if Config.STORAGE_CHANNEL:
        try:
            caption = f"📂 {file_name}\n🗃 {file_size}\n👤 {user}\n🔗 {link}"
            await client.send_document(Config.STORAGE_CHANNEL, document=path, caption=caption)
        except Exception as e:
            logger.warning(f"Failed to backup to STORAGE_CHANNEL: {e}")
