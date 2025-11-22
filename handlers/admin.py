
# handlers/admin.py
from pyrogram import filters
from config import Config
import logging

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    @app.on_message(filters.command("checkchannels") & filters.private)
    async def check_channels(client, message):
        """Check if bot can access configured channels"""
        from pyrogram import enums
        results = []
        has_errors = False
        
        # Check LOG_CHANNEL
        if Config.LOG_CHANNEL:
            try:
                chat = await client.get_chat(Config.LOG_CHANNEL)
                results.append(f"✅ LOG_CHANNEL: {chat.title} ({Config.LOG_CHANNEL})")
            except Exception as e:
                has_errors = True
                error_msg = "Bot not added to channel" if "Peer id invalid" in str(e) else str(e)
                results.append(f"❌ LOG_CHANNEL ({Config.LOG_CHANNEL}): {error_msg}")
        else:
            results.append("⚠️ LOG_CHANNEL not configured")
        
        # Check ERROR_CHANNEL
        if Config.ERROR_CHANNEL:
            try:
                chat = await client.get_chat(Config.ERROR_CHANNEL)
                results.append(f"✅ ERROR_CHANNEL: {chat.title} ({Config.ERROR_CHANNEL})")
            except Exception as e:
                has_errors = True
                error_msg = "Bot not added to channel" if "Peer id invalid" in str(e) else str(e)
                results.append(f"❌ ERROR_CHANNEL ({Config.ERROR_CHANNEL}): {error_msg}")
        else:
            results.append("⚠️ ERROR_CHANNEL not configured")
        
        # Check STORAGE_CHANNEL
        if Config.STORAGE_CHANNEL:
            try:
                chat = await client.get_chat(Config.STORAGE_CHANNEL)
                results.append(f"✅ STORAGE_CHANNEL: {chat.title} ({Config.STORAGE_CHANNEL})")
            except Exception as e:
                has_errors = True
                error_msg = "Bot not added to channel" if "Peer id invalid" in str(e) else str(e)
                results.append(f"❌ STORAGE_CHANNEL ({Config.STORAGE_CHANNEL}): {error_msg}")
        else:
            results.append("⚠️ STORAGE_CHANNEL not configured")
        
        response = "<b>📊 Channel Status:</b>\n\n" + "\n".join(results)
        
        if has_errors:
            response += "\n\n<b>💡 How to fix:</b>\n1. Open your channel in Telegram\n2. Click channel name → Administrators\n3. Add your bot as admin\n4. Grant 'Post Messages' permission\n5. Run /checkchannels again"
        
        await message.reply(response, parse_mode=enums.ParseMode.HTML)
