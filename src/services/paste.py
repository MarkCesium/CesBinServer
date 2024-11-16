from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from time import time

from src.services.files import FileService
from src.core.models import Paste, Period
from src.core.repositories import PeriodRepository
from src.core.config import BASE_DIR
from src.core.exceptions.paste import PasteCreateError


class PasteService:
    @classmethod
    async def create(
        cls, session: AsyncSession, text: str, period_name: str | None = None
    ) -> int:
        paste = Paste()
        path = f"pastes/{time()*1000}.txt"
        paste.path = str(path)

        if period_name is not None:
            period: Period = await PeriodRepository.get_one_or_none(
                session, name=period_name
            )
            if period is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Period not found")
            paste.expire_at = paste.created_at + period.duration

        try:
            await FileService.create(str(BASE_DIR / path), text)
        except Exception as e:
            await session.close()
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

        session.add(paste)
        await session.commit()

        return paste.id
