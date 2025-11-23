# handlers/auto_delete.py
import logging
from pyrogram import filters
from pyrogram.types import Message
from Theinertbotz.database import db
from script import Script

log = logging.getLogger("TeraBoxBot")

def parse_time(time_str: str) -> int:
    """Parse time string to seconds. Format: 30s, 5m, 1h"""
    if not time_str:
        return None
    
    time_str = time_str.strip().lower()
    
    if time_str.endswith('s'):
        return int(time_str[:-1])
    elif time_str.endswith('m'):
        return int(time_str[:-1]) * 60
    elif time_str.endswith('h'):
        return int(time_str[:-1]) * 3600
    else:
        return None

def format_time(seconds: int) -> str:
    """Convert seconds to formatted string"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    else:
        return f"{seconds // 3600}h"

def register_handlers(app):
    @app.on_message(filters.private & filters.command("auto_delete"))
    async def auto_delete_handler(client, message: Message):
        """Toggle auto-delete on/off or show status"""
        try:
            user_id = message.from_user.id
            args = message.text.split()
            
            if len(args) > 1:
                action = args[1].lower()
                
                if action == "on":
                    # Enable auto-delete with default 5 seconds
                    db.set_user_auto_delete(user_id, True)
                    await message.reply(Script.AUTO_DELETE_ENABLED, parse_mode="HTML")
                    log.info(f"User {user_id} enabled auto_delete")
                    
                elif action == "off":
                    # Disable auto-delete
                    db.set_user_auto_delete(user_id, False)
                    await message.reply(Script.AUTO_DELETE_DISABLED, parse_mode="HTML")
                    log.info(f"User {user_id} disabled auto_delete")
                    
                else:
                    await message.reply("❌ Invalid option. Use: <code>/auto_delete on</code> or <code>/auto_delete off</code>", parse_mode="HTML")
            else:
                # Show current status
                current_setting = db.get_user_auto_delete(user_id)
                if current_setting:
                    await message.reply(Script.AUTO_DELETE_ENABLED, parse_mode="HTML")
                else:
                    await message.reply(Script.AUTO_DELETE_DISABLED, parse_mode="HTML")
            
        except Exception as e:
            log.exception("auto_delete_handler error")
            await message.reply("❌ Error updating setting", parse_mode="HTML")
    
    @app.on_message(filters.private & filters.command("set_auto_delete"))
    async def set_auto_delete_handler(client, message: Message):
        """Set custom auto-delete time"""
        try:
            user_id = message.from_user.id
            args = message.text.split()
            
            if len(args) < 2:
                await message.reply(Script.SET_AUTO_DELETE_USAGE, parse_mode="HTML")
                return
            
            time_str = args[1]
            seconds = parse_time(time_str)
            
            if seconds is None or seconds <= 0:
                await message.reply(f"❌ Invalid time format. Use: 30s, 5m, 1h\n\nExample: <code>/set_auto_delete 5m</code>", parse_mode="HTML")
                return
            
            # Save to global settings (applies to all users)
            db.set_auto_delete_time(seconds)
            db.set_user_auto_delete(user_id, True)
            
            response = f"✅ <b>ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ sᴇᴛ</b>\n\n⏱️ Messages will auto-delete in <b>{format_time(seconds)}</b> to help prevent copyright issues."
            await message.reply(response, parse_mode="HTML")
            log.info(f"Auto-delete time set to {seconds} seconds")
            
        except Exception as e:
            log.exception("set_auto_delete_handler error")
            await message.reply("❌ Error setting auto-delete time", parse_mode="HTML")
    
    @app.on_message(filters.private & filters.command("remove_auto_delete"))
    async def remove_auto_delete_handler(client, message: Message):
        """Disable auto-delete completely"""
        try:
            user_id = message.from_user.id
            
            # Disable auto-delete
            db.set_user_auto_delete(user_id, False)
            db.set_auto_delete_time(None)
            
            response = "⏹️ <b>ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴅɪsᴀʙʟᴇᴅ</b>\n\n💾 Video messages will be saved permanently."
            await message.reply(response, parse_mode="HTML")
            log.info(f"User {user_id} removed auto_delete")
            
        except Exception as e:
            log.exception("remove_auto_delete_handler error")
            await message.reply("❌ Error disabling auto-delete", parse_mode="HTML")

