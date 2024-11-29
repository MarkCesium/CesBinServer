from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from time import time

from src.services.files import FileService
from src.core.models import Paste, Period, Format
from src.core.repositories import (
    PeriodRepository,
    FormatRepository,
    PasteRepository,
)
from src.core.config import BASE_DIR
from src.tasks.tasks import delete_paste


class PasteService:
    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        text: str,
        format_name: str,
        period_name: str | None = None,
    ) -> int:
        paste = Paste()
        path = f"pastes/{time()*1000}.txt"
        paste.path = str(path)

        format: Format | None = await FormatRepository.get_one_or_none(
            session, name=format_name
        )
        if format is None:
            await session.close()
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Format not found")

        paste.format_id = format.id

        session.add(paste)
        await session.flush([paste])

        if period_name is not None:
            period: Period = await PeriodRepository.get_one_or_none(
                session, name=period_name
            )
            if period is None:
                await session.close()
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Period not found")
            paste.expire_at = paste.created_at + period.duration

        try:
            await FileService.create(str(BASE_DIR / path), text)
        except Exception:
            await session.close()
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

        await session.commit()

        if paste.expire_at is not None:
            delete_paste.apply_async((paste.id,), eta=paste.expire_at)

        return paste.id

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> str:
        paste: Paste = await PasteRepository.get_by_id(session, id)
        if paste is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        text: str = await FileService.get(str(BASE_DIR / paste.path))
        format: Format = await FormatRepository.get_by_id(session, paste.format_id)

        return {
            "id": paste.id,
            "text": text,
            "created_at": paste.created_at,
            "expire_at": paste.expire_at if paste.expire_at is not None else None,
            "format": format.name,
        }
