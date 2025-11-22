# core/router.py
# Responsible for registering all handlers into the Pyrogram Client.
# It imports the handlers' register functions and calls them exactly once.

from handlers.start import register_handlers as register_start
from handlers.download_handler import register_handlers as register_download

def register_all(app):
    """
    Call each handler's register function once.
    Keep this simple and explicit to avoid recursion.
    """
    register_start(app)
    register_download(app)
