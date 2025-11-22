from pyrogram import filters, enums
import logging
from Theinertbotz.database import db
from script import Script

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    @app.on_message(filters.command("rename") & filters.private)
    async def rename_cmd(client, message):
        user_id = message.from_user.id
        args = message.text.split()
        
        if len(args) < 2:
            # Show current setting
            current = db.get_user_rename_setting(user_id)
            custom = db.get_custom_rename_pattern(user_id)
            
            if custom and "{" in custom:
                status_text = f"Custom: <code>{custom}</code>"
            elif current == "timestamp":
                status_text = "Timestamp (YYYYMMDD_HHMMSS)"
            elif current == "datetime":
                status_text = "DateTime (YYYY-MM-DD_HH-MM-SS)"
            else:
                status_text = "Disabled"
            
            help_text = Script.RENAME_HELP_TEXT.format(status=status_text)
            await message.reply(help_text, parse_mode=enums.ParseMode.HTML)
            return
        
        command = args[1].lower()
        
        if command in ["on", "yes", "enable", "timestamp"]:
            db.set_user_rename_setting(user_id, "timestamp")
            await message.reply(Script.RENAME_ON, parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} enabled auto-rename (timestamp)")
        
        elif command == "datetime":
            db.set_user_rename_setting(user_id, "datetime")
            await message.reply(Script.RENAME_DATETIME, parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} enabled auto-rename (datetime)")
        
        elif command in ["off", "no", "disable"]:
            db.set_user_rename_setting(user_id, "")
            await message.reply(Script.RENAME_OFF, parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} disabled auto-rename")
        
        else:
            await message.reply(Script.INVALID_OPTION, parse_mode=enums.ParseMode.HTML)
    
    @app.on_message(filters.command("set_rename") & filters.private)
    async def set_rename_cmd(client, message):
        user_id = message.from_user.id
        try:
            # Extract pattern from command
            cmd_parts = message.text.split(maxsplit=1)
            if len(cmd_parts) < 2:
                await message.reply(Script.CUSTOM_PATTERN_USAGE, parse_mode=enums.ParseMode.HTML)
                return
            
            pattern = cmd_parts[1].strip()
            
            # Validate pattern contains at least one variable
            if "{" not in pattern:
                await message.reply(Script.CUSTOM_PATTERN_ERROR, parse_mode=enums.ParseMode.HTML)
                return
            
            # Save custom pattern
            db.set_custom_rename_pattern(user_id, pattern)
            await message.reply(Script.CUSTOM_PATTERN_SAVED.format(pattern=pattern), parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} set custom rename pattern: {pattern}")
        
        except Exception as e:
            log.exception("set_rename error")
            await message.reply(f"❌ Error: {str(e)}", parse_mode=enums.ParseMode.HTML)
