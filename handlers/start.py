from pyrogram import filters, enums
import logging

START_TEXT = """
<b>👋 Welcome!</b>

Send me any valid TeraBox link.
"""

def register_handlers(app):
    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        try:
            await message.reply(START_TEXT, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("start handler error")
