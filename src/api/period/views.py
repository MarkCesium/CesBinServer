from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_helper import db_helper
from src.core.repositories import PeriodRepository

from . import schemas

router = APIRouter(prefix="/period", tags=["Periods"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_periods(
    session: AsyncSession = Depends(db_helper.async_session_dependency),
) -> list[schemas.PeriodRead]:
    return await PeriodRepository.get_all(session)
