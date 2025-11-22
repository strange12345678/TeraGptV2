# core/router.py
from plugins.command import register_commands
from handlers.download_handler import register_handlers as register_download
from handlers.rename import register_handlers as register_rename
from handlers.admin import register_handlers as register_admin

def register_all(app):
    register_commands(app)
    register_rename(app)
    register_download(app)
    register_admin(app)
