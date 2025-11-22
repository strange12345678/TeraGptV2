from .start import register_handlers as _start
from .download_handler import register_handlers as _download

def register_all(app):
    _start(app)
    _download(app)
