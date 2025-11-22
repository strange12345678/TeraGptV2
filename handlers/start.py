from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from Theinertbotz.database import db

START_TEXT = """
<b>🎬 TeraBox Downloader Bot</b>

<b>⚡ Ultra-Fast File Downloads</b>

Simply send a <code>TeraBox</code> link and I'll:
✅ Download the file instantly
✅ Send it directly to your chat
✅ Generate thumbnails for videos
✅ Track download progress
✅ Support all file types

<b>📝 Quick Start:</b>
<code>https://1024terabox.com/s/1abc123def456ghi</code>

<b>🎛️ Advanced Features:</b>
• <code>/rename</code> - Customize file naming
• <code>/set_rename &lt;pattern&gt;</code> - Custom patterns
• <code>/help</code> - View all commands

<b>💡 Pro Tips:</b>
💬 Send multiple links at once
🎬 Videos get automatic thumbnails
⚡ Progress tracked in real-time
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📚 Commands", callback_data="help")],
    [InlineKeyboardButton("🔄 Rename Settings", callback_data="rename_help")],
    [InlineKeyboardButton("⚙️ About", callback_data="about")]
])

COMMANDS_TEXT = """
<b>📋 Available Commands:</b>

<b>/start</b> - Show this welcome message
<b>/rename</b> - View rename settings
<b>/set_rename &lt;pattern&gt;</b> - Set custom naming pattern
<b>/help</b> - Show this message

<b>📌 Rename Variables:</b>
• {file_name} • {file_size}
• {username} • {user_id}
• {date} • {time} • {timestamp}
"""

ABOUT_TEXT = """
<b>ℹ️ About TeraBox Bot</b>

A powerful Telegram bot for downloading files from TeraBox with:

✨ <b>Features:</b>
• Lightning-fast downloads
• Automatic video thumbnails
• Custom file naming
• Real-time progress tracking
• Multi-file support

🛠️ <b>Built with:</b>
Pyrogram • Python 3.11 • MongoDB

📊 <b>Status:</b>
✅ All systems operational

"""

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
            await message.reply(START_TEXT, reply_markup=START_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("start handler error")
    
    @app.on_message(filters.command("help") & filters.private)
    async def help_cmd(client, message):
        try:
            await message.reply(COMMANDS_TEXT, parse_mode=enums.ParseMode.HTML)
        except Exception:
            logging.getLogger("TeraBoxBot").exception("help handler error")