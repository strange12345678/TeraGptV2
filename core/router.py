# core/router.py
from handlers.start import register_handlers as register_start
from handlers.download_handler import register_handlers as register_download

def register_all(app):
    register_start(app)
    register_download(app)
