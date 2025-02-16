from .format.views import router as format_router
from .paste.views import router as paste_router

__all__ = ("paste_router", "format_router")
