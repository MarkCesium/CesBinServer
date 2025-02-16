from fastapi import APIRouter

from .format.views import router as format_router
from .paste.views import router as paste_router
from .period.views import router as period_router

api_router = APIRouter(prefix="/api")
api_router.include_router(format_router)
api_router.include_router(paste_router)
api_router.include_router(period_router)

__all__ = ("api_router",)
