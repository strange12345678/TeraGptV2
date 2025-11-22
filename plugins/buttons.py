# plugins/buttons.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Start command buttons
START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📚 Commands", callback_data="help")],
    [InlineKeyboardButton("🔄 Rename Settings", callback_data="rename_help")],
    [InlineKeyboardButton("⚙️ About", callback_data="about")]
])

# Help command buttons (with back to start)
HELP_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔄 Rename Help", callback_data="rename_help")],
    [InlineKeyboardButton("⚙️ About", callback_data="about")],
    [InlineKeyboardButton("← Back to Menu", callback_data="start")]
])

# Rename help buttons (with back to help)
RENAME_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("← Back to Commands", callback_data="help")]
])

# About buttons (with back to help)
ABOUT_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("← Back to Commands", callback_data="help")]
])

__all__ = ["START_BUTTONS", "HELP_BUTTONS", "RENAME_BUTTONS", "ABOUT_BUTTONS"]
