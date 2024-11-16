from .base import BaseRepository
from src.core.models import Period


class PeriodRepository(BaseRepository):
    model = Period
