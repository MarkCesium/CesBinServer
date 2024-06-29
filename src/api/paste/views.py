from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas
from .dependency import get_paste_dependency
from src.core.db_helper import db_helper
from src.core.models import Paste

router = APIRouter(prefix="/paste", tags=["Paste"])


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_paste(
    paste: schemas.PasteRead = Depends(get_paste_dependency),
) -> schemas.PasteRead:
    return paste


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_paste(
    paste: schemas.PasteCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> schemas.PasteRead:
    return await crud.create_paste(session, paste)
