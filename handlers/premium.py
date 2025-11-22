# handlers/premium.py
from pyrogram import filters, enums
import logging
from Theinertbotz.database import db
from script import Script
from plugins.premium import PremiumManager
from plugins.buttons import PREMIUM_BUTTONS, PREMIUM_STATUS_BUTTONS, PREMIUM_UPGRADE_BUTTONS

log = logging.getLogger("TeraBoxBot")

def register_handlers(app):
    @app.on_message(filters.command("premium") & filters.private)
    async def premium_cmd(client, message):
        try:
            await message.reply(Script.PREMIUM_TEXT, reply_markup=PREMIUM_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("premium_cmd error")
    
    @app.on_callback_query(filters.regex("^premium$"))
    async def premium_callback(client, callback_query):
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.PREMIUM_TEXT, reply_markup=PREMIUM_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("premium_callback error")
    
    @app.on_callback_query(filters.regex("^premium_status$"))
    async def premium_status_callback(client, callback_query):
        try:
            user_id = callback_query.from_user.id
            status = PremiumManager.get_user_status(user_id)
            text = Script.PREMIUM_STATUS.format(status=status)
            await callback_query.answer()
            await callback_query.message.edit_text(text, reply_markup=PREMIUM_STATUS_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("premium_status_callback error")
    
    @app.on_callback_query(filters.regex("^premium_upgrade$"))
    async def premium_upgrade_callback(client, callback_query):
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.UPGRADE_TEXT, reply_markup=PREMIUM_UPGRADE_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("premium_upgrade_callback error")

__all__ = ["register_handlers"]
