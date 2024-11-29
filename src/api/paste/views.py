from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from src.core.db_helper import db_helper
from src.services import PasteService

router = APIRouter(prefix="/paste", tags=["Paste"])


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_paste(
    id: int,
    session: AsyncSession = Depends(db_helper.async_session_dependency),
) -> schemas.PasteRead:
    return await PasteService.get(session, id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_paste(
    paste: schemas.PasteCreate,
    session: AsyncSession = Depends(db_helper.async_session_dependency),
) -> schemas.PasteRead:
    id = await PasteService.create(session, paste.text, paste.format, paste.period)

    return await PasteService.get(session, id)
