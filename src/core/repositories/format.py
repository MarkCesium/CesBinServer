from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Format

from .base import BaseRepository


class FormatRepository(BaseRepository[Format]):
    def __init__(self, session: AsyncSession):
        super().__init__(Format, session)
