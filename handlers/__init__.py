# handlers/__init__.py
# Simple explicit exports to make imports clear and avoid circular references.

from .start import register_handlers as register_start
from .download_handler import register_handlers as register_download

__all__ = ["register_start", "register_download"]
