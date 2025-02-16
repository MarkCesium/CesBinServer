from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_helper import db_helper
from src.core.repositories import FormatRepository

from . import schemas

router = APIRouter(prefix="/format", tags=["Format"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_formats(
    session: AsyncSession = Depends(db_helper.async_session_dependency),
) -> list[schemas.FormatRead]:
    return await FormatRepository.get_all(session)
