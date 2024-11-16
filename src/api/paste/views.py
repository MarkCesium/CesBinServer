from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from src.core.config import BASE_DIR
from src.core.db_helper import db_helper
from src.core.repositories import PasteRepository, FormatRepository
from src.core.models import Paste, Format
from src.services import PasteService, FileService

router = APIRouter(prefix="/paste", tags=["Paste"])


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_paste(
    id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> schemas.PasteRead:
    return await PasteService.get(session, id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_paste(
    paste: schemas.PasteCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> schemas.PasteRead:
    id = await PasteService.create(session, paste.text, paste.format, paste.period)

    return await PasteService.get(session, id)
