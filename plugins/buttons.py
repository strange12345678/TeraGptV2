# plugins/buttons.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Start command buttons
START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📚 Commands", callback_data="help")],
    [InlineKeyboardButton("🔄 Rename Settings", callback_data="rename_help")],
    [InlineKeyboardButton("⚙️ About", callback_data="about")]
])

# Rename command buttons
RENAME_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("⚡ Quick Options", callback_data="rename_quick")],
    [InlineKeyboardButton("✨ Custom Pattern", callback_data="rename_custom")],
    [InlineKeyboardButton("← Back", callback_data="help")]
])

# Help command buttons
HELP_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔄 Rename Help", callback_data="rename_help")],
    [InlineKeyboardButton("⚙️ About", callback_data="about")],
    [InlineKeyboardButton("← Back", callback_data="help")]
])

__all__ = ["START_BUTTONS", "RENAME_BUTTONS", "HELP_BUTTONS"]
