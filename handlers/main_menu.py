# handlers/main_menu.py
from pyrogram import filters, enums
import logging
from script import Script
from plugins.buttons import MAIN_MENU, PREMIUM_BUTTONS, HELP_BUTTONS

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    """Register main menu button handlers."""
    
    # ===== Dashboard Button =====
    @app.on_message(filters.text & filters.regex("^📊 ᴅᴀꜱʜʙᴏᴀʀᴅ$") & filters.private)
    async def dashboard_handler(client, message):
        try:
            await message.reply(Script.DASHBOARD_TEXT, reply_markup=MAIN_MENU, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("dashboard_handler error")
    
    # ===== Support Button =====
    @app.on_message(filters.text & filters.regex("^💬 ꜱᴜᴘᴘᴏʀᴛ 💬$") & filters.private)
    async def support_handler(client, message):
        try:
            await message.reply(
                "📞 <b>Support Channel</b>\n\nClick the link below to join our support community:",
                reply_markup=__import__('pyrogram').types.InlineKeyboardMarkup([
                    [__import__('pyrogram').types.InlineKeyboardButton("💬 Join Support Chat", url="https://t.me/TheInertBotzchat")],
                    [__import__('pyrogram').types.InlineKeyboardButton("← Back to Menu", callback_data="back_to_menu")]
                ]),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            log.exception("support_handler error")
    
    # ===== Update Button =====
    @app.on_message(filters.text & filters.regex("^🔄 ᴜᴘᴅᴀᴛᴇ 🔄$") & filters.private)
    async def update_handler(client, message):
        try:
            await message.reply(
                "🔄 <b>Updates & News</b>\n\nFollow for latest updates:",
                reply_markup=__import__('pyrogram').types.InlineKeyboardMarkup([
                    [__import__('pyrogram').types.InlineKeyboardButton("📢 Follow Updates", url="https://t.me/theinertbotz")],
                    [__import__('pyrogram').types.InlineKeyboardButton("← Back to Menu", callback_data="back_to_menu")]
                ]),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            log.exception("update_handler error")
    
    # ===== Premium Button =====
    @app.on_message(filters.text & filters.regex("^💎 ᴘʀᴇᴍɪᴜᴍ 💎$") & filters.private)
    async def premium_button_handler(client, message):
        try:
            await message.reply(Script.PREMIUM_INFO, reply_markup=PREMIUM_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("premium_button_handler error")
    
    # ===== Help Button =====
    @app.on_message(filters.text & filters.regex("^❓ ʜᴇʟᴘ$") & filters.private)
    async def help_button_handler(client, message):
        try:
            await message.reply(Script.COMMANDS_TEXT, reply_markup=HELP_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("help_button_handler error")
    
    # ===== Settings Button =====
    @app.on_message(filters.text & filters.regex("^⚙️ sᴇᴛᴛɪɴɢs ⚙️$") & filters.private)
    async def settings_handler(client, message):
        try:
            await message.reply(Script.SETTINGS_TEXT, reply_markup=__import__('pyrogram').types.InlineKeyboardMarkup([
                [__import__('pyrogram').types.InlineKeyboardButton("← Back to Menu", callback_data="back_to_menu")]
            ]), parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("settings_handler error")
    
    # ===== About Button =====
    @app.on_message(filters.text & filters.regex("^ℹ️ ᴀʙᴏᴜᴛ ℹ️$") & filters.private)
    async def about_button_handler(client, message):
        try:
            await message.reply(Script.ABOUT_TEXT, reply_markup=__import__('pyrogram').types.InlineKeyboardMarkup([
                [__import__('pyrogram').types.InlineKeyboardButton("← Back to Menu", callback_data="back_to_menu")]
            ]), parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("about_button_handler error")
    
    # ===== Back to Menu Callback =====
    @app.on_callback_query(filters.regex("^back_to_menu$"))
    async def back_to_menu_callback(client, callback_query):
        try:
            await callback_query.answer()
            await callback_query.message.delete()
        except Exception:
            log.exception("back_to_menu_callback error")

__all__ = ["register_handlers"]
