from .base import BaseRepository, BaseSyncRepository
from src.core.models import Paste


class PasteRepository(BaseRepository):
    model = Paste


class PasteSyncRepository(BaseSyncRepository):
    model = Paste
