from datetime import datetime, timezone
from time import time

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import BASE_DIR
from src.core.db_helper import db_helper
from src.core.models import Format, Paste, Period
from src.core.repositories import (
    FormatRepository,
    PasteRepository,
    PasteSyncRepository,
    PeriodRepository,
)
from src.services.files import FileService
from src.tasks.celery import celery_app


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
        paste.path = f"pastes/{time()*1000}.txt"

        format: Format | None = await FormatRepository.get_one_or_none(
            session, name=format_name
        )
        if format is None:
            await session.close()
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Format not found")

        paste.format_id = format.id
        paste.created_at = datetime.now(timezone.utc)

        try:
            await FileService.create(str(BASE_DIR / paste.path), text)
        except Exception:
            await session.close()
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        
        if period_name is not None:
            period: Period = await PeriodRepository.get_one_or_none(
                session, name=period_name
            )
            if period is None:
                await session.close()
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Period not found")
            
            paste.expire_at = paste.created_at + period.duration

        session.add(paste)
        await session.commit()

        if paste.expire_at is not None:
            delete_paste.apply_async((paste.id,), eta=paste.expire_at)

        return paste

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


@celery_app.task
def delete_paste(id: int) -> None:
    with db_helper.sync_session_factory() as session:
        paste: Paste = PasteSyncRepository.get_by_id(session, id)
        FileService.delete(str(BASE_DIR / paste.path))
        session.delete(paste)
        session.commit()
