# handlers/main_menu.py
from pyrogram import filters, enums
from pyrogram.enums import ChatAction
import logging
from script import Script
from plugins.buttons import MAIN_MENU, PREMIUM_BUTTONS, HELP_BUTTONS, DASHBOARD_BACK_BUTTON

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    """Register main menu button handlers."""
    
    # ===== Dashboard Callback =====
    @app.on_callback_query(filters.regex("^dashboard$"))
    async def dashboard_callback(client, callback_query):
        try:
            from Theinertbotz.database import db
            from config import Config
            from datetime import datetime
            
            user_id = callback_query.from_user.id
            user_name = callback_query.from_user.first_name or "User"
            
            # Get user data
            tier = db.get_user_tier(user_id)
            premium_status = "✅ Premium" if tier == "premium" and db.is_premium_valid(user_id) else "❌ Free"
            expiry = db.get_premium_expiry(user_id)
            if expiry:
                exp_date = datetime.fromisoformat(expiry).strftime("%d/%m/%Y")
                premium_expiry = exp_date
            else:
                premium_expiry = "Permanent" if tier == "premium" else "N/A"
            
            today_downloads = db.get_daily_downloads(user_id)
            total_downloads = db.get_total_downloads(user_id)
            success_rate = db.get_success_rate()
            
            # Format dashboard text
            dashboard_text = Script.DASHBOARD_TEXT.format(
                user_name=user_name,
                user_id=user_id,
                premium_status=premium_status,
                premium_expiry=premium_expiry,
                today_downloads=today_downloads,
                total_downloads=total_downloads,
                total_data_used="N/A",
                storage_remaining="N/A",
                api_status="🟢 Online",
                ping_ms="≈50",
                bot_uptime="Running",
                workers_active=Config.WORKERS,
                queue_size="0",
                task_success_rate=success_rate,
                bot_name="TeraBox Bot"
            )
            
            await callback_query.answer()
            # Show typing indicator for smooth transition
            await client.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
            await callback_query.message.edit_text(dashboard_text, reply_markup=DASHBOARD_BACK_BUTTON, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("dashboard_callback error")
    
    # ===== Premium Callback =====
    @app.on_callback_query(filters.regex("^premium$"))
    async def premium_callback(client, callback_query):
        try:
            await callback_query.answer()
            # Show typing indicator for smooth transition
            await client.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
            await callback_query.message.edit_text(Script.PREMIUM_INFO, reply_markup=PREMIUM_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("premium_callback error")
    
    # ===== Help Callback (from Help button in main menu) =====
    @app.on_callback_query(filters.regex("^help$"))
    async def help_callback(client, callback_query):
        try:
            await callback_query.answer()
            # Show typing indicator for smooth transition
            await client.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
            await callback_query.message.edit_text(Script.COMMANDS_TEXT, reply_markup=HELP_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("help_callback error")
    
    # ===== Settings Callback =====
    @app.on_callback_query(filters.regex("^settings$"))
    async def settings_callback(client, callback_query):
        try:
            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            await callback_query.answer()
            # Show typing indicator for smooth transition
            await client.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
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
            # Show typing indicator for smooth transition
            await client.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
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
            # Show typing indicator for smooth transition
            await client.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
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
