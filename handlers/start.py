# handlers/start.py
# Start command handler - moved to plugins/command.py
# This file is kept for compatibility but delegates to the command plugin

from plugins.command import register_commands

def register_handlers(app):
    """Register start command handlers by delegating to command plugin."""
    register_commands(app)