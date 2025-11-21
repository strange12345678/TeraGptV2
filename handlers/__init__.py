from . import start, download_handler

def register_all(app):
    start.register_handlers(app)
    download_handler.register_handlers(app)
