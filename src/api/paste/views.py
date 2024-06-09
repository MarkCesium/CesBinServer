from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas
from src.core.db_helper import db_helper
from src.core.models import Paste
from uuid import uuid4
from time import time

router = APIRouter(prefix="/paste", tags=["Paste"])


@router.get("/{id}")
async def get_paste(
    id: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> schemas.Paste:
    # TODO: Extract it in depenency
    paste = await crud.get_paste(session, id)
    if paste is not None:
        return paste
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post("/")
async def create_paste(
    data: schemas.PasteCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> schemas.Paste:
    return await crud.create_paste(
        session,
        Paste(**data.model_dump(), id=str(uuid4()), created_at=round(time() * 1000)),
    )
