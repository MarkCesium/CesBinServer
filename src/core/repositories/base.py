from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, Result


class BaseRepository:
    model = None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        return await session.get(cls.model, id)

    @classmethod
    async def get_all(cls, session: AsyncSession, **filter_by):
        return await session.scalars(Select(cls.model).filter_by(**filter_by))

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filter_by):
        query = Select(cls.model).filter_by(**filter_by)
        result: Result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, session: AsyncSession, **data):
        entity = cls.model(**data)
        session.add(entity)
        await session.commit()
