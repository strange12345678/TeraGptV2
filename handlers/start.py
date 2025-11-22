from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from Theinertbotz.database import db
from script import Script

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📚 Commands", callback_data="help")],
    [InlineKeyboardButton("🔄 Rename Settings", callback_data="rename_help")],
    [InlineKeyboardButton("⚙️ About", callback_data="about")]
])

def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(client, message):
        from plugins.log_channel import log_action
        user_id = message.from_user.id
        is_new = db.add_user(user_id)

        if is_new:
            username = message.from_user.username or message.from_user.first_name or "Unknown"
            await log_action(client, user_id, f"🆕 New User: @{username}")

        try:
            await message.reply(Script.START_TEXT, reply_markup=START_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("start handler error")
    
    @app.on_message(filters.command("help") & filters.private)
    async def help_cmd(client, message):
        try:
            await message.reply(Script.COMMANDS_TEXT, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("help handler error")
    
    @app.on_callback_query(filters.regex("^help$"))
    async def help_callback(client, callback_query):
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.COMMANDS_TEXT, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("help callback error")
    
    @app.on_callback_query(filters.regex("^rename_help$"))
    async def rename_help_callback(client, callback_query):
        try:
            user_id = callback_query.from_user.id
            current = db.get_user_rename_setting(user_id)
            custom = db.get_custom_rename_pattern(user_id)
            
            if custom and "{" in custom:
                status = f"Custom: <code>{custom}</code>"
            elif current == "timestamp":
                status = "Timestamp (YYYYMMDD_HHMMSS)"
            elif current == "datetime":
                status = "DateTime (YYYY-MM-DD_HH-MM-SS)"
            else:
                status = "Disabled"
            
            text = Script.RENAME_HELP_TEXT.format(status=status)
            await callback_query.answer()
            await callback_query.message.edit_text(text, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("rename_help callback error")
    
    @app.on_callback_query(filters.regex("^about$"))
    async def about_callback(client, callback_query):
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.ABOUT_TEXT, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("about callback error")