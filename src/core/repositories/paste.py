from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Paste

from .base import BaseRepository, BaseSyncRepository


class PasteRepository(BaseRepository[Paste]):
    def __init__(self, session: AsyncSession):
        super().__init__(Paste, session)


class PasteSyncRepository(BaseSyncRepository):
    model = Paste
