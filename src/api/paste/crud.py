from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.core.models import Paste
from . import schemas
from uuid import uuid4
from time import time


async def get_paste_list(session: AsyncSession) -> list[Paste]:
    result: Result = await session.execute(select(Paste).order_by(Paste.created_at))
    return result.scalars().all()


async def get_paste(session: AsyncSession, id: str) -> Paste:
    return await session.get(Paste, id)


async def create_paste(session: AsyncSession, paste: schemas.PasteCreate) -> Paste:
    entity = Paste(
        **paste.model_dump(), id=str(uuid4()), created_at=round(time() * 1000)
    )
    session.add(entity)
    await session.commit()
    return entity
