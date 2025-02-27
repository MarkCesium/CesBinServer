import logging
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import Result, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

T = TypeVar("T")
logger = logging.getLogger(__name__)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def get_by_id(self, id: int) -> Optional[T]:
        return await self.session.get(self.model, id)
    
    async def get_all(self, **filter_by) -> list[T]:
        return await self.session.scalars(select(self.model).filter_by(**filter_by))

    async def get_one_or_none(self, **filter_by) -> Optional[T]:
        query = select(self.model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, **data) -> T:
        entity = self.model(**data)
        self.session.add(entity)
        await self.session.commit()
        return entity
    
    async def update(self, id: int, **data) -> Optional[T]:
        result = await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, id: int) -> None:
        await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.commit()


class BaseSyncRepository:
    model = None

    @classmethod
    def get_by_id(cls, session: Session, id: int):
        return session.get(cls.model, id)

    @classmethod
    def get_all(cls, session: Session, **filter_by):
        return session.query(cls.model).filter_by(**filter_by)

    @classmethod
    def get_one_or_none(cls, session: Session, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result: Result = session.execute(query)
        return result.scalar_one_or_none()
