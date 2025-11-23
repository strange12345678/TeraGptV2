# handlers/auto_delete.py
import logging
from pyrogram import filters
from pyrogram.types import Message
from Theinertbotz.database import db
from script import Script

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    @app.on_message(filters.private & filters.command("auto_delete"))
    async def auto_delete_handler(client, message: Message):
        """Toggle auto-delete messages for current user"""
        try:
            user_id = message.from_user.id
            
            # Get current setting
            current_setting = db.get_user_auto_delete(user_id)
            new_setting = not current_setting
            
            # Update setting
            db.set_user_auto_delete(user_id, new_setting)
            
            # Send response
            if new_setting:
                response = Script.AUTO_DELETE_ENABLED
            else:
                response = Script.AUTO_DELETE_DISABLED
            
            await message.reply(response, parse_mode="HTML")
            log.info(f"User {user_id} set auto_delete to {new_setting}")
            
        except Exception as e:
            log.exception("auto_delete_handler error")
            await message.reply("❌ Error updating setting", parse_mode="HTML")

