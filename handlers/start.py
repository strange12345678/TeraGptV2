from pyrogram import filters
import logging

START_TEXT = """
<b>👋 Welcome!</b>

Send me any valid TeraBox link.
"""

def register_handlers(app):
    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        try:
            # use lowercase 'html'
            await message.reply(START_TEXT, parse_mode="html")
        except Exception:
            logging.getLogger("TeraBoxBot").exception("start handler error")
