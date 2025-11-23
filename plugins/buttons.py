# plugins/buttons.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Main menu (Reply Keyboard - persistent at bottom)
MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("📊 ᴅᴀꜱʜʙᴏᴀʀᴅ")
        ],
        [
            KeyboardButton("💬 ꜱᴜᴘᴘᴏʀᴛ 💬"), KeyboardButton("🔄 ᴜᴘᴅᴀᴛᴇ 🔄")
        ],
        [
            KeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ 💎"), KeyboardButton("❓ ʜᴇʟᴘ")
        ],
        [
            KeyboardButton("⚙️ sᴇᴛᴛɪɴɢs ⚙️"), KeyboardButton("ℹ️ ᴀʙᴏᴜᴛ ℹ️")
        ]
    ],
    resize_keyboard=True
)

# Start command buttons (inline)
START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📚 Commands", callback_data="help")],
    [InlineKeyboardButton("🔄 Rename Settings", callback_data="rename_help")],
    [InlineKeyboardButton("💎 Premium", callback_data="premium")]
])

# Help command buttons (with back to start)
HELP_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔄 Rename Help", callback_data="rename_help")],
    [InlineKeyboardButton("💎 Premium", callback_data="premium")],
    [InlineKeyboardButton("← Back to Menu", callback_data="start")]
])

# Rename help buttons (with back to help)
RENAME_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("← Back to Commands", callback_data="help")]
])

# Premium buttons
PREMIUM_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("👤 My Status", callback_data="premium_status")],
    [InlineKeyboardButton("← Back to Commands", callback_data="help")]
])

# Premium status buttons
PREMIUM_STATUS_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💳 Upgrade", callback_data="premium_upgrade")],
    [InlineKeyboardButton("← Back", callback_data="premium")]
])

# Upgrade buttons
PREMIUM_UPGRADE_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📸 Send Screenshot to Admin", url="https://t.me/darkworld008")],
    [InlineKeyboardButton("← Back", callback_data="premium_status")]
])

# Admin panel buttons
ADMIN_PANEL_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("👥 Manage Premium Users", callback_data="admin_manage")],
    [InlineKeyboardButton("🔍 Check User Status", callback_data="admin_check")],
    [InlineKeyboardButton("← Back to Commands", callback_data="help")]
])

# Admin manage buttons
ADMIN_MANAGE_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Add Premium User", callback_data="admin_add_premium")],
    [InlineKeyboardButton("➖ Remove Premium User", callback_data="admin_remove_premium")],
    [InlineKeyboardButton("← Back", callback_data="admin_panel")]
])

# Admin settings buttons
ADMIN_SETTINGS_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("♻️ Auto-Delete", callback_data="admin_auto_delete")],
    [InlineKeyboardButton("← Back", callback_data="admin_panel")]
])

__all__ = ["MAIN_MENU", "START_BUTTONS", "HELP_BUTTONS", "RENAME_BUTTONS", "PREMIUM_BUTTONS", "PREMIUM_STATUS_BUTTONS", "PREMIUM_UPGRADE_BUTTONS", "ADMIN_PANEL_BUTTONS", "ADMIN_MANAGE_BUTTONS", "ADMIN_SETTINGS_BUTTONS"]
