from .base import BaseRepository
from src.core.models import Format


class FormatRepository(BaseRepository):
    model = Format
