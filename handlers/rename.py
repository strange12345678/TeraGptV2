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
<b>🔄 Auto-Rename Settings</b>

<b>Current Status:</b> {status_text}

━━━━━━━━━━━━━━━━━━━━

<b>⚡ Quick Options:</b>
<code>/rename on</code> - Timestamp (YYYYMMDD_HHMMSS)
<code>/rename datetime</code> - DateTime (YYYY-MM-DD_HH-MM-SS)
<code>/rename off</code> - Disable renaming

<b>✨ Custom Naming:</b>
<code>/set_rename &lt;your_pattern&gt;</code>

<b>📝 Available Variables:</b>
{{file_name}} • {{file_size}} • {{username}}
{{user_id}} • {{date}} • {{time}}
{{timestamp}} • {{ext}}

<b>💡 Pattern Examples:</b>
<code>@Theinertbotz_{{file_name}}_{{file_size}}</code>
→ @Theinertbotz_video_42MB.mp4

<code>{{username}}_{{date}}_{{file_name}}</code>
→ admin_2025-11-22_video.mp4

<code>Archive_{{timestamp}}</code>
→ Archive_20251122_082326.zip

━━━━━━━━━━━━━━━━━━━━
"""
            await message.reply(help_text, parse_mode=enums.ParseMode.HTML)
            return
        
        command = args[1].lower()
        
        if command in ["on", "yes", "enable", "timestamp"]:
            db.set_user_rename_setting(user_id, "timestamp")
            await message.reply(
                "✅ <b>Auto-rename Enabled</b>\n\n"
                "📌 Format: <code>filename_YYYYMMDD_HHMMSS.ext</code>\n"
                "💾 Applied to all downloads\n"
                "Type <code>/rename</code> to change", 
                parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} enabled auto-rename (timestamp)")
        
        elif command == "datetime":
            db.set_user_rename_setting(user_id, "datetime")
            await message.reply(
                "✅ <b>Auto-rename Enabled</b>\n\n"
                "📌 Format: <code>filename_YYYY-MM-DD_HH-MM-SS.ext</code>\n"
                "💾 Applied to all downloads\n"
                "Type <code>/rename</code> to change", 
                parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} enabled auto-rename (datetime)")
        
        elif command in ["off", "no", "disable"]:
            db.set_user_rename_setting(user_id, "")
            await message.reply(
                "❌ <b>Auto-rename Disabled</b>\n\n"
                "📌 Files will keep original names\n"
                "Use <code>/rename on</code> to enable again", 
                parse_mode=enums.ParseMode.HTML)
            log.info(f"User {user_id} disabled auto-rename")
        
        else:
            await message.reply(
                "❓ <b>Unknown Option</b>\n\n"
                "Type <code>/rename</code> for help or examples.", 
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
                f"✅ <b>Custom Pattern Saved!</b>\n\n"
                f"📝 <b>Your Pattern:</b>\n"
                f"<code>{pattern}</code>\n\n"
                f"💾 <b>Applied to:</b> All future downloads\n\n"
                f"📌 <b>Example:</b>\n"
                f"<code>your_renamed_file.mp4</code>",
                parse_mode=enums.ParseMode.HTML
            )
            log.info(f"User {user_id} set custom rename pattern: {pattern}")
        
        except Exception as e:
            log.exception("set_rename error")
            await message.reply(f"❌ Error: {str(e)}", parse_mode=enums.ParseMode.HTML)
