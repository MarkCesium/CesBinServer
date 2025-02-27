from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, status

from src.providers import get_period_repository

from . import schemas

if TYPE_CHECKING:
    from src.core.repositories import PeriodRepository
    
router = APIRouter(prefix="/period", tags=["Periods"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_periods(
    period_repository: Annotated["PeriodRepository", Depends(get_period_repository)],
) -> list[schemas.PeriodRead]:
    return await period_repository.get_all()
