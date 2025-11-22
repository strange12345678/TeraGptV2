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
            custom = db.get_custom_rename_pattern(user_id)
            
            if custom and "{" in custom:
                status_text = f"Custom: <code>{custom}</code>"
            elif current == "timestamp":
                status_text = "Timestamp (YYYYMMDD_HHMMSS)"
            elif current == "datetime":
                status_text = "DateTime (YYYY-MM-DD_HH-MM-SS)"
            else:
                status_text = "Disabled"
            
            help_text = f"""
<b>🔄 Auto-Rename Feature</b>

<b>Current Status:</b> {status_text}

<b>Preset Options:</b>
• <code>/rename on</code> - Enable timestamp
• <code>/rename datetime</code> - DateTime format
• <code>/rename off</code> - Disable

<b>Custom Pattern:</b>
• <code>/set_rename &lt;pattern&gt;</code> - Set custom pattern

<b>Available Variables:</b>
• <code>{{file_name}}</code> - Original filename
• <code>{{file_size}}</code> - File size
• <code>{{username}}</code> - Your username
• <code>{{user_id}}</code> - Your user ID
• <code>{{date}}</code> - Current date (YYYY-MM-DD)
• <code>{{time}}</code> - Current time (HH-MM-SS)
• <code>{{timestamp}}</code> - Full timestamp
• <code>{{ext}}</code> - File extension

<b>Examples:</b>
<code>/set_rename @Theinertbotz_{{file_name}}_{{file_size}}</code>
<code>/set_rename {{username}}_{{date}}_{{file_name}}</code>
<code>/set_rename Video_{{timestamp}}</code>
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
        
        elif command in ["off", "no", "disable"]:
            db.set_user_rename_setting(user_id, "")
            await message.reply("❌ Auto-rename <b>disabled</b>. Files will keep original names.", 
                              parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} disabled auto-rename")
        
        else:
            await message.reply("❌ Invalid option. Type <code>/rename</code> for help.", 
                              parse_mode=enums.ParseMode.HTML)
    
    @app.on_message(filters.command("set_rename") & filters.private)
    async def set_rename_cmd(client, message):
        user_id = message.from_user.id
        try:
            # Extract pattern from command
            cmd_parts = message.text.split(maxsplit=1)
            if len(cmd_parts) < 2:
                await message.reply(
                    "❌ <b>Usage:</b> <code>/set_rename &lt;pattern&gt;</code>\n\n"
                    "Example: <code>/set_rename @Theinertbotz_{{file_name}}_{{file_size}}</code>\n\n"
                    "Type <code>/rename</code> for available variables.",
                    parse_mode=enums.ParseMode.HTML
                )
                return
            
            pattern = cmd_parts[1].strip()
            
            # Validate pattern contains at least one variable
            if "{" not in pattern:
                await message.reply(
                    "❌ Pattern must contain at least one variable.\n"
                    "Example: <code>/set_rename @Bot_{{file_name}}_{{file_size}}</code>",
                    parse_mode=enums.ParseMode.HTML
                )
                return
            
            # Save custom pattern
            db.set_custom_rename_pattern(user_id, pattern)
            
            await message.reply(
                f"✅ Custom rename pattern set!\n\n"
                f"<b>Pattern:</b> <code>{pattern}</code>\n\n"
                f"<b>Example output:</b>\n"
                f"<code>@Bot_myvideo_19.4MB.mp4</code>",
                parse_mode=enums.ParseMode.HTML
            )
            log.info(f"User {user_id} set custom rename pattern: {pattern}")
        
        except Exception as e:
            log.exception("set_rename error")
            await message.reply(f"❌ Error: {str(e)}", parse_mode=enums.ParseMode.HTML)
