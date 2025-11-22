
# handlers/admin.py
from pyrogram import filters
from config import Config
import logging

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    @app.on_message(filters.command("checkchannels") & filters.private)
    async def check_channels(client, message):
        """Check if bot can access configured channels"""
        results = []
        
        # Check LOG_CHANNEL
        if Config.LOG_CHANNEL:
            try:
                chat = await client.get_chat(Config.LOG_CHANNEL)
                results.append(f"✅ LOG_CHANNEL: {chat.title} ({Config.LOG_CHANNEL})")
            except Exception as e:
                results.append(f"❌ LOG_CHANNEL ({Config.LOG_CHANNEL}): {str(e)}")
        else:
            results.append("⚠️ LOG_CHANNEL not configured")
        
        # Check ERROR_CHANNEL
        if Config.ERROR_CHANNEL:
            try:
                chat = await client.get_chat(Config.ERROR_CHANNEL)
                results.append(f"✅ ERROR_CHANNEL: {chat.title} ({Config.ERROR_CHANNEL})")
            except Exception as e:
                results.append(f"❌ ERROR_CHANNEL ({Config.ERROR_CHANNEL}): {str(e)}")
        else:
            results.append("⚠️ ERROR_CHANNEL not configured")
        
        # Check STORAGE_CHANNEL
        if Config.STORAGE_CHANNEL:
            try:
                chat = await client.get_chat(Config.STORAGE_CHANNEL)
                results.append(f"✅ STORAGE_CHANNEL: {chat.title} ({Config.STORAGE_CHANNEL})")
            except Exception as e:
                results.append(f"❌ STORAGE_CHANNEL ({Config.STORAGE_CHANNEL}): {str(e)}")
        else:
            results.append("⚠️ STORAGE_CHANNEL not configured")
        
        response = "<b>📊 Channel Status:</b>\n\n" + "\n".join(results)
        await message.reply(response)
