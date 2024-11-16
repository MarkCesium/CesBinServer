from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from time import time

from . import schemas
from src.core.config import BASE_DIR
from src.core.db_helper import db_helper
from src.core.repositories import PasteRepository
from src.core.models import Paste
from src.services.paste import PasteService
from src.services.files import FileService

router = APIRouter(prefix="/paste", tags=["Paste"])


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_paste(
    id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> schemas.PasteRead:
    paste: Paste = await PasteRepository.get_by_id(session, id)
    if paste is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    text = await FileService.get(str(BASE_DIR / paste.path))
    return schemas.PasteRead(
        id=paste.id,
        text=text,
        created_at=paste.created_at,
        expire_at=paste.expire_at if paste.expire_at is not None else None,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_paste(
    paste: schemas.PasteCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> schemas.PasteRead:
    id = await PasteService.create(session, paste.text, paste.period)
    paste: Paste = await PasteRepository.get_by_id(session, id)
    text = await FileService.get(str(BASE_DIR / paste.path))

    return schemas.PasteRead(
        id=paste.id,
        text=text,
        created_at=paste.created_at,
        expire_at=paste.expire_at if paste.expire_at is not None else None,
    )
