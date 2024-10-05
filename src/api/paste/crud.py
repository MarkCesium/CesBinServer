from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.core.models import Paste
from src.core.config import BASE_DIR
from . import schemas
from time import time
from src.services.files import create_paste_file, get_paste_from_file


async def get_paste_list(session: AsyncSession) -> list[Paste]:
    """
    Currently NOT in use
    """
    result: Result = await session.execute(select(Paste).order_by(Paste.created_at))
    return result.scalars().all()


async def get_paste(session: AsyncSession, id: int) -> schemas.PasteRead | None:
    paste = await session.get(Paste, id)
    if paste is None:
        return None
    return schemas.PasteRead(
        id=paste.id,
        text=await get_paste_from_file(paste.paste_path),
        created_at=paste.created_at,
        expire_at=paste.expire_at,
    )


async def create_paste(
    session: AsyncSession, paste: schemas.PasteCreate
) -> schemas.PasteRead:
    # Do NOT use it
    # TODO: Rewrite this function with Period model
    path = BASE_DIR / "pastes" / f"{id}.txt"
    entity = Paste(
        paste_path=str(path),
        created_at=round(time() * 1000),
        expire_at=paste.expire_at,
    )
    try:
        await create_paste_file(entity.paste_path, paste.text)
    except Exception:
        raise Exception("Failed to create paste file")
    session.add(entity)
    await session.commit()
    return schemas.PasteRead(
        **paste.model_dump(), id=entity.id, created_at=entity.created_at
    )
