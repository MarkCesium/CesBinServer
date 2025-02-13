from src.core.models import Paste

from .base import BaseRepository, BaseSyncRepository


class PasteRepository(BaseRepository):
    model = Paste


class PasteSyncRepository(BaseSyncRepository):
    model = Paste
