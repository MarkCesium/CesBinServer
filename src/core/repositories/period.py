from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Period

from .base import BaseRepository


class PeriodRepository(BaseRepository[Period]):
    def __init__(self, session: AsyncSession):
        super().__init__(Period, session)
