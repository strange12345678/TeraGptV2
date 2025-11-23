# handlers/main_menu.py
from pyrogram import filters, enums
import logging
from script import Script
from plugins.buttons import MAIN_MENU, PREMIUM_BUTTONS, HELP_BUTTONS

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    """Register main menu button handlers."""
    
    # ===== Dashboard Callback =====
    @app.on_callback_query(filters.regex("^dashboard$"))
    async def dashboard_callback(client, callback_query):
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.DASHBOARD_TEXT, reply_markup=MAIN_MENU, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("dashboard_callback error")
    
    # ===== Premium Callback =====
    @app.on_callback_query(filters.regex("^premium$"))
    async def premium_callback(client, callback_query):
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.PREMIUM_INFO, reply_markup=PREMIUM_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("premium_callback error")
    
    # ===== Help Callback (from Help button in main menu) =====
    @app.on_callback_query(filters.regex("^help$"))
    async def help_callback(client, callback_query):
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.COMMANDS_TEXT, reply_markup=HELP_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("help_callback error")
    
    # ===== Settings Callback =====
    @app.on_callback_query(filters.regex("^settings$"))
    async def settings_callback(client, callback_query):
        try:
            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            await callback_query.answer()
            await callback_query.message.edit_text(Script.SETTINGS_TEXT, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("← Back to Menu", callback_data="back_to_menu")]
            ]), parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("settings_callback error")
    
    # ===== About Callback =====
    @app.on_callback_query(filters.regex("^about$"))
    async def about_callback(client, callback_query):
        try:
            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            await callback_query.answer()
            await callback_query.message.edit_text(Script.ABOUT_TEXT, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("← Back to Menu", callback_data="back_to_menu")]
            ]), parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("about_callback error")
    
    # ===== Back to Menu Callback =====
    @app.on_callback_query(filters.regex("^back_to_menu$"))
    async def back_to_menu_callback(client, callback_query):
        try:
            await callback_query.answer()
            # Delete the current message and send a new one with the main menu
            await callback_query.message.delete()
            await client.send_message(
                chat_id=callback_query.message.chat.id,
                text=Script.START_TEXT,
                reply_markup=MAIN_MENU,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            log.exception("back_to_menu_callback error")

__all__ = ["register_handlers"]
