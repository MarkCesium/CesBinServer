from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories import FormatRepository, PasteRepository, PeriodRepository
from src.services import PasteService

from .core.db_helper import db_helper


def get_paste_repository(session: Annotated[AsyncSession, Depends(db_helper.async_session_dependency)]) -> PasteRepository:
    return PasteRepository(session)


def get_format_repository(session: Annotated[AsyncSession, Depends(db_helper.async_session_dependency)]) -> FormatRepository:
    return FormatRepository(session)

def get_period_repository(session: Annotated[AsyncSession, Depends(db_helper.async_session_dependency)]) -> PeriodRepository:
    return PeriodRepository(session)

def get_paste_service(
        paste_repository: Annotated[PasteRepository, Depends(get_paste_repository)],
        format_repository: Annotated[FormatRepository, Depends(get_format_repository)],
        period_repository: Annotated[PeriodRepository, Depends(get_period_repository)],
    ) -> PasteService:
    return PasteService(paste_repository, format_repository, period_repository)