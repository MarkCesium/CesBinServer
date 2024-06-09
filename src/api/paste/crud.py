from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.core.models import Paste


async def get_paste(session: AsyncSession, id: str) -> Paste:
    return await session.get(Paste, id)


async def create_paste(session: AsyncSession, paste: Paste) -> Paste:
    session.add(paste)
    await session.commit()
    return paste
