from pyrogram import filters, enums
import logging

START_TEXT = """
<b>👋 Welcome!</b>

Send me any valid TeraBox link.
"""

def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(client, message):
        from plugins.log_channel import log_action
        user_id = message.from_user.id
        is_new = db.add_user(user_id)

        # Log only new users
        if is_new:
            username = message.from_user.username or message.from_user.first_name or "Unknown"
            await log_action(client, user_id, f"🆕 New User: @{username}")

        try:
            await message.reply(START_TEXT, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("start handler error")