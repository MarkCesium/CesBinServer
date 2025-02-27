import logging
from datetime import datetime, timezone
from time import time

from fastapi import status
from fastapi.exceptions import HTTPException

from src.core.config import BASE_DIR
from src.core.db_helper import db_helper
from src.core.models import Paste
from src.core.repositories import (
    FormatRepository,
    PasteRepository,
    PasteSyncRepository,
    PeriodRepository,
)
from src.services.files import FileService
from src.tasks.celery import celery_app

logger = logging.getLogger(__name__)

class PasteService:
    def __init__(self, paste_repository: PasteRepository, format_repository: FormatRepository, period_repository: PeriodRepository):
        self.paste_repository = paste_repository
        self.format_repository = format_repository
        self.period_repository = period_repository
    
    async def create(
        self,
        text: str,
        format_name: str,
        period_name: str | None = None,
    ) -> int:
        data = dict()
        data["path"] = f"pastes/{time()*1000}.txt"

        format = await self.format_repository.get_one_or_none(name=format_name)
        if format is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Format not found")

        data["format_id"] = format.id
        data["created_at"] = datetime.now(timezone.utc)

        try:
            await FileService.create(str(BASE_DIR / data["path"]), text)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        
        if period_name is not None:
            period = await self.period_repository.get_one_or_none(name=period_name)
            if period is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Period not found")
            
            data["expire_at"] = data["created_at"] + period.duration

        paste = await self.paste_repository.create(**data)
        if paste.expire_at is not None:
            delete_paste.apply_async((paste.id,), eta=paste.expire_at)
            logger.debug("Created at: %s, expire at: %s", paste.created_at, paste.expire_at)
        
        return paste

    async def get(self, id: int) -> dict:
        paste = await self.paste_repository.get_by_id(id)
        if paste is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        text = await FileService.get(str(BASE_DIR / paste.path))
        format = await self.format_repository.get_by_id(paste.format_id)

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
