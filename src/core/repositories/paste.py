from .base import BaseRepository
from src.core.models import Paste


class PasteRepository(BaseRepository):
    model = Paste
