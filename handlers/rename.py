from pyrogram import filters, enums
import logging
from Theinertbotz.database import db

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    @app.on_message(filters.command("rename") & filters.private)
    async def rename_cmd(client, message):
        user_id = message.from_user.id
        args = message.text.split()
        
        if len(args) < 2:
            # Show current setting
            current = db.get_user_rename_setting(user_id)
            status_text = "Enabled (Timestamp)" if current == "timestamp" else \
                         "Enabled (DateTime)" if current == "datetime" else \
                         "Disabled"
            
            help_text = f"""
<b>🔄 Auto-Rename Feature</b>

<b>Current Status:</b> {status_text}

<b>Available Options:</b>
• <code>/rename on</code> - Enable with timestamp (default)
• <code>/rename timestamp</code> - Timestamp pattern (YYYYMMDD_HHMMSS)
• <code>/rename datetime</code> - DateTime pattern (YYYY-MM-DD_HH-MM-SS)
• <code>/rename off</code> - Disable auto-rename

<b>Examples:</b>
• <code>video.mp4</code> → <code>video_20251122_082326.mp4</code> (timestamp)
• <code>video.mp4</code> → <code>video_2025-11-22_08-23-26.mp4</code> (datetime)
"""
            await message.reply(help_text, parse_mode=enums.ParseMode.HTML)
            return
        
        command = args[1].lower()
        
        if command in ["on", "yes", "enable", "timestamp"]:
            db.set_user_rename_setting(user_id, "timestamp")
            await message.reply("✅ Auto-rename <b>enabled</b> (Timestamp format: YYYYMMDD_HHMMSS)", 
                              parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} enabled auto-rename (timestamp)")
        
        elif command == "datetime":
            db.set_user_rename_setting(user_id, "datetime")
            await message.reply("✅ Auto-rename <b>enabled</b> (DateTime format: YYYY-MM-DD_HH-MM-SS)", 
                              parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} enabled auto-rename (datetime)")
        
        elif command in ["off", "no", "disable", ""]:
            db.set_user_rename_setting(user_id, "")
            await message.reply("❌ Auto-rename <b>disabled</b>. Files will keep original names.", 
                              parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} disabled auto-rename")
        
        else:
            await message.reply("❌ Invalid option. Use: <code>/rename on</code>, <code>/rename datetime</code>, or <code>/rename off</code>", 
                              parse_mode=enums.ParseMode.HTML)
