# core/router.py
from plugins.command import register_commands
from handlers.download_handler import register_handlers as register_download
from handlers.rename import register_handlers as register_rename
from handlers.premium import register_handlers as register_premium
from handlers.admin import register_handlers as register_admin
from handlers.main_menu import register_handlers as register_main_menu
from handlers.auto_delete import register_handlers as register_auto_delete

def register_all(app):
    register_commands(app)
    register_main_menu(app)
    register_rename(app)
    register_premium(app)
    register_download(app)
    register_admin(app)
    register_auto_delete(app)
