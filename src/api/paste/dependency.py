from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path
from src.core.db_helper import db_helper
from typing import Annotated


async def get_paste_dependency(
    id: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    paste = await crud.get_paste(session, id)
    if paste is not None:
        return paste
    raise HTTPException(status.HTTP_404_NOT_FOUND)
